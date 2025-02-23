import os
import sys
import uuid

import anyio
import dagger
from kubernetes import client as k8s_client, config

DEPLOYMENT_NAME = "nautilus"


def create_deployment_object(image: str):
    container = k8s_client.V1Container(
        name=DEPLOYMENT_NAME,
        image=image,
        volume_mounts=[
            k8s_client.V1VolumeMount(
                name=f"{DEPLOYMENT_NAME}-config",
                mount_path=f"/home/{DEPLOYMENT_NAME}/config/",
            ),
            k8s_client.V1VolumeMount(
                name=f"{DEPLOYMENT_NAME}-config-storage",
                mount_path=f"/home/{DEPLOYMENT_NAME}/config_storage/",
            )
        ],
    )

    template = k8s_client.V1PodTemplateSpec(
        metadata=k8s_client.V1ObjectMeta(
            name=DEPLOYMENT_NAME, labels={"app": DEPLOYMENT_NAME}
        ),
        spec=k8s_client.V1PodSpec(
            containers=[container],
            volumes=[
                k8s_client.V1Volume(
                    name=f"{DEPLOYMENT_NAME}-config",
                    config_map=k8s_client.V1ConfigMapEnvSource(
                        name=f"{DEPLOYMENT_NAME}-config"
                    ),
                ),
                k8s_client.V1Volume(
                    name=f"{DEPLOYMENT_NAME}-config-storage",
                    persistent_volume_claim=k8s_client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=f"{DEPLOYMENT_NAME}-config-storage"
                    ),
                )
            ],
        ),
    )

    spec = k8s_client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={"matchLabels": {"app": DEPLOYMENT_NAME}},
    )

    deployment = k8s_client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=k8s_client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec,
    )

    return deployment


def update_deployment(api: k8s_client.AppsV1Api, deployment: k8s_client.V1Deployment):
    response = api.patch_namespaced_deployment(
        name=DEPLOYMENT_NAME, namespace="suprachat", body=deployment
    )

    print(f"Deployment {DEPLOYMENT_NAME} updated.")
    print(
        f"Namespace: {response.metadata.namespace}\n"
        f"Name: {response.metadata.namespace}\n"
        f"Revision: {response.metadata.generation}\n"
        f"Image: {response.spec.template.spec.containers[0].image}\n"
    )


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        venv_cache = client.cache_volume("venv")

        # Stage 1: Test, typecheck and lint
        test = (
            client.container()
            .from_("python:3.11.3-slim-bullseye")
            .with_workdir("/usr/src/app")
            .with_exec(["apt-get", "-qq", "update", "-y"])
            .with_exec(
                [
                    "apt-get",
                    "-qq",
                    "install",
                    "-y",
                    "build-essential",
                ]
            )
            .with_directory(
                path="/usr/src/app",
                directory=client.host().directory(
                    ".",
                    include=["nautilus", "poetry.lock", "pyproject.toml", "README.md"],
                ),
            )
            .with_exec(["pip", "install", "poetry==1.5.1"])
            .with_exec(["pip", "install", "--upgrade", "pip", "wheel", "setuptools"])
            .with_exec(["poetry", "config", "virtualenvs.in-project", "true"])
            .with_mounted_cache("/usr/src/app/.venv", venv_cache)
            .with_exec(["poetry", "install"])
        )

        lint_output = await test.with_exec(
            ["poetry", "run", "ruff", "check", f"{DEPLOYMENT_NAME}/"]
        ).stdout()

        typecheck_output = await test.with_exec(
            ["poetry", "run", "pyright", f"{DEPLOYMENT_NAME}/"]
        ).stdout()

        test_output = await test.with_exec(["poetry", "run", "pytest"]).stdout()

        print(lint_output)
        print(typecheck_output)
        print(test_output)

        if os.getenv("CI_PIPELINE_SOURCE") != "merge_request_event":

            # Stage 2: Build
            build = test.with_exec(["poetry", "install", "--only", "main"]).with_exec(
                ["poetry", "build", "--format=wheel"]
            )

            build_output = await build.stdout()

            wheel_filename = (
                [string for string in build_output.split("\n") if ".whl" in string][0]
                .replace("- Built ", "")
                .strip()
            )

            container = (
                client.container()
                .from_("python:3.11.3-slim-bullseye")
                .with_workdir("/usr/src/app")
                .with_file(
                    f"/usr/src/app/{wheel_filename}",
                    build.directory("/usr/src/app/dist").file(wheel_filename),
                )
                .with_exec(["pip", "install", f"./{wheel_filename}"])
                .with_exec(["useradd", "-ms", "/usr/sbin/nologin", "nautilus"])
                .with_workdir("/home/nautilus")
                .with_entrypoint(["sopel"])
                .with_user("nautilus")
                .with_default_args(["-c", "config_storage/config.cfg"])
            )

            print(await container.stdout())

            image_ref = await container.publish(f"ttl.sh/nautilus-{uuid.uuid4()}:2h")

            print(f"Published image to {image_ref}")

            # Stage 3: Deploy to Kubernetes
            config.load_config()
            apps_v1 = k8s_client.AppsV1Api()

            deployment = create_deployment_object(image_ref)

            update_deployment(
                apps_v1,
                deployment,
            )


if __name__ == "__main__":
    anyio.run(main)
