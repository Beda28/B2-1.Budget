from pathlib      import Path
from dataclasses  import asdict
from .model       import Transaction
from .repository  import JsonlRepository

class TransactionService:
    def __init__(self, data_dir: str = "./data"):
        self.transaction = JsonlRepository(Path(data_dir)/"transactions.jsonl")
        self.category    = JsonlRepository(Path(data_dir)/"categorys.jsonl")
        self.budget      = JsonlRepository(Path(data_dir)/"budgets.jsonl")

    def next_id(self) -> int:
        return self.transaction.next_id()

    def add(self, transaction: Transaction) -> None:
        self.transaction.save(transaction)

    def list(self, limit: int | None = None) -> list[dict]:
        data = list(self.transaction.stream())
        if limit is not None and limit > 0: data = data[-limit:]
        return data

    def detail(self, id: int) -> dict | None:
        data_list = self.transaction.stream()

        for data in data_list:
            if data["id"] == id:
                return data
        return None

    def update(self, id: int, data: Transaction) -> bool:
        return self.transaction.update(id, asdict(data))
    
    def delete(self, id: int) -> bool:
        return self.transaction.delete(id)