from pathlib    import Path
from model      import Transaction
from repository import JsonlRepository

class TransactionService:
    def __init__(self, data_dir: str = "./data"):
        self.repository = JsonlRepository(Path(data_dir)/"transactions.jsonl")

    def add(self, transaction: Transaction) -> None:
        self.repository.save(transaction)