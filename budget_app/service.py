from pathlib    import Path
from model      import Transaction
from repository import JsonlRepository

class TransactionService:
    def __init__(self, data_dir: str = "./data"):
        self.repository = JsonlRepository(Path(data_dir)/"transactions.jsonl")

    def next_id(self) -> int:
        return self.repository.next_id()

    def add(self, transaction: Transaction) -> None:
        self.repository.save(transaction)

    def list(self) -> list[dict]:
        return list(self.repository.stream())

    def detail(self, id: int) -> dict | None:
        data_list = self.repository.stream()

        for data in data_list:
            if data["id"] == id:
                return data

        return None