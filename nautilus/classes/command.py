from dataclasses import dataclass
from typing import Callable

from ..utils.exceptions import (
    MissingRequiredArgs,
    ExceedingArgs,
    RequiredArgsAfterOptionalArgs,
)
from .param import Param


@dataclass
class Command:
    params: list[Param]
    action: Callable

    def exec(self, args: list[str]):
        for index, param in enumerate(self.params):
            if index > 0 and param.required and not self.params[index - 1].required:
                raise RequiredArgsAfterOptionalArgs

        required_params = [param for param in self.params if param.required]
        total_args_qty = len(self.params)
        significant_args = args[2:]

        passed_args_diff = len(required_params) - len(significant_args)

        if total_args_qty - len(required_params) < 0:
            raise ExceedingArgs
        if passed_args_diff > 0:
            raise MissingRequiredArgs(
                required_params[len(required_params) - passed_args_diff :]
            )
        else:
            self.action(*significant_args)
