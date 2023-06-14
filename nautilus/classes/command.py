from dataclasses import dataclass
from typing import Callable

from ..utils.exceptions import MissingRequiredArgs, ExceedingArgs
from .param import Param


@dataclass
class Command:
    params: list[Param]
    action: Callable

    def exec(self, args: list[str]):
        print(args)
        required_args_qty = len([param for param in self.params if param.required])
        total_args_qty = len(self.params)
        significant_args = args[2:]

        print(significant_args)

        passed_args_diff = required_args_qty - len(significant_args)

        print(passed_args_diff)

        if total_args_qty - required_args_qty < 0:
            print(total_args_qty, required_args_qty)
            raise ExceedingArgs
        if passed_args_diff > 0:
            print(self.params)
            raise MissingRequiredArgs(self.params[passed_args_diff - 1])
        else:
            self.action(*significant_args)
