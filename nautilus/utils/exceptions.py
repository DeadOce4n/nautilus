from ..classes.param import Param


class UserNotFound(Exception):
    pass


class MissingRequiredArgs(Exception):
    def __init__(self, missing_args: Param | list[Param]):
        self.missing_args = missing_args


class ExceedingArgs(Exception):
    pass
