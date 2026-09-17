from pathlib      import Path
from dataclasses  import asdict
from collections  import defaultdict
from .model       import Transaction
from .repository  import JsonlRepository

class TransactionService:
    def __init__(self, data_dir: str = "./data"):
        self.transaction = JsonlRepository(Path(data_dir)/"transactions.jsonl")
        self.category    = JsonlRepository(Path(data_dir)/"categories.jsonl")
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

    def category_add(self, name: str) -> None:
        self.category.save({"name": name})
        
    def category_list(self) -> list[dict]:
        return list(self.category.stream())

    def category_remove(self, name: str) -> bool:
        category = self.category_list()

        for cate in category:
            if cate["name"] == name:
                category.remove(cate)
                self.category.rewrite(category)
                return True
        return False

    def budget_set(self, month: str, amount: int) -> None:
        data = list(self.budget.stream())

        for item in data:
            if item["month"] == month:
                item["amount"] = amount
                self.budget.rewrite(data)
                return

        data.append({
            "month": month,
            "amount": amount
        })

        self.budget.rewrite(data)

    def summary(self, month: str, top: int = 3) -> dict:
        total_income   = 0
        total_expense  = 0
        category_total = defaultdict(int)

        for data in self.transaction.stream():
            if   not data["date"].startswith(month): continue
            if   data["type"] == "income": total_income += data["amount"]
            elif data["type"] == "expense": 
                total_expense += data["amount"]
                category_total[data["category"]] += data["amount"]

        budget_amount = 0

        for data in self.budget.stream():
            if data["month"] == month:
                budget_amount = data["amount"]
                break

        top_categories = sorted(
            category_total.items(),
            key=lambda item: item[1],
            reverse=True
        )[:top]

        return {
            "month"          : month,
            "total_income"   : total_income,
            "total_expense"  : total_expense,
            "balance"        : total_income - total_expense,
            "budget"         : budget_amount,
            "top_categories" : top_categories
        }

    def search(self, date_from: str | None = None, date_to: str | None = None,
                     category : str | None = None, type   : str | None = None, 
                     q        : str | None = None, tag    : str | None = None
            ) -> list[dict]:
        data_list = []

        for data in self.transaction.stream():
            if date_from is not None and data["date"]      < date_from: continue
            if date_to   is not None and data["date"]      > date_to  : continue
            if category  is not None and data["category"] != category : continue
            if type      is not None and data["type"]     != type     : continue
            if q         is not None and data["memo"]     != q        : continue
            if tag       is not None and data["tags"]     != tag      : continue

            data_list.append(data)
        data_list.sort(key=lambda item: item["date"], reverse=True)

        return data_list