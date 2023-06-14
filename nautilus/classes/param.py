from dataclasses import dataclass


@dataclass
class Param:
    name: str
    required: bool = False
