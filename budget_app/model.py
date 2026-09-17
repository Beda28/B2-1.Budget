from dataclasses import dataclass, field
from typing      import Literal

@dataclass
class Transaction:
    id: int
    type: Literal["income", "expense"]
    date: str
    amount: int
    category: str
    memo: str = ""
    tags: list[str] = field(default_factory=list)

@dataclass
class Category:
    name: str

@dataclass
class Budget:
    month: str
    amount: int