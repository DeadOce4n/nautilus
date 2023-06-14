__version__ = "0.1.0"
from . import nautilus  # noqa: F401

import socket
from requests.packages.urllib3.util import connection as urllib3_cn  # type: ignore


def allowed_gai_family():
    return socket.AF_INET


urllib3_cn.allowed_gai_family = allowed_gai_family
