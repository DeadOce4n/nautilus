from ..classes.param import Param


class UserNotFound(Exception):
    def __init__(self, username: str | None = None):
        self.username = username


class MissingRequiredArgs(Exception):
    def __init__(self, missing_args: Param | list[Param]):
        self.missing_args = missing_args


class ExceedingArgs(Exception):
    pass


class RequiredArgsAfterOptionalArgs(Exception):
    pass

class UnrecognizedArgs(Exception):
    def __init__(self, unrecognized_args: list[str]):
        self.unrecognized_args = unrecognized_args
