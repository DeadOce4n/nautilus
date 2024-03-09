from dataclasses import dataclass
from typing import Callable

from ..utils.exceptions import MissingRequiredArgs, ExceedingArgs
from .param import Param


@dataclass
class Command:
    params: list[Param]
    action: Callable

    def exec(self, args: list[str]):
        required_args_qty = len([param for param in self.params if param.required])
        total_args_qty = len(self.params)
        significant_args = args[2:]

        passed_args_diff = required_args_qty - len(significant_args)

        if total_args_qty - required_args_qty < 0:
            raise ExceedingArgs
        if passed_args_diff > 0:
            print(passed_args_diff)
            print(self.params)
            raise MissingRequiredArgs(self.params[-passed_args_diff])
        else:
            self.action(*significant_args)
