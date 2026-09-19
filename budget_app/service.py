from pathlib      import Path
from dataclasses  import asdict
from collections  import defaultdict
from .model       import Transaction
from .repository  import JsonlRepository
from .validate    import (
    validate_date,
    validate_month,
    validate_amount,
    validate_type,
    validate_category_name,
    validate_memo,
    validate_tags,
    validate_limit,
    validate_top,
    validate_id,
    validate_date_range,
    validate_csv_file,
    validate_export_condition
)


class TransactionService:
    def __init__(self, data_dir: str = "./data"):
        self.transaction = JsonlRepository(Path(data_dir)/"transactions.jsonl")
        self.category    = JsonlRepository(Path(data_dir)/"categories.jsonl")
        self.budget      = JsonlRepository(Path(data_dir)/"budgets.jsonl")

    def next_id(self) -> int:
        return self.transaction.next_id()

    def category_exists(self, name: str) -> bool:
        return any(
            data["name"] == name
            for data in self.category.stream()
        )

    def validate_transaction_category(self, category: str) -> None:
        if not self.category_exists(category):
            raise ValueError(f"등록되지 않은 카테고리입니다: {category}\n먼저 category add로 등록해주세요.")

    def add(self, transaction: Transaction) -> None:
        validate_date(transaction.date)
        validate_amount(transaction.amount)
        validate_type(transaction.type)
        validate_category_name(transaction.category)
        validate_memo(transaction.memo)
        validate_tags(transaction.tags)
        self.validate_transaction_category(transaction.category)
        
        self.transaction.save(transaction)

    def list(self, limit: int = 3) -> list[dict]:
        validate_limit(limit)

        data = list(self.transaction.stream())
        if limit is not None: data = data[-limit:]

        data.sort(key=lambda item: (item["date"], item["id"]), reverse=True)
        return data

    def detail(self, id: int) -> dict | None:
        validate_id(id)
        data_list = self.transaction.stream()

        for data in data_list:
            if data["id"] == id:
                return data
        return None

    def update(self, id: int, data: Transaction) -> bool:
        validate_id(id)
        validate_date(data.date)
        validate_amount(data.amount)
        validate_type(data.type)
        validate_category_name(data.category)
        validate_memo(data.memo)
        validate_tags(data.tags)
        self.validate_transaction_category(data.category)

        return self.transaction.update(id, asdict(data))
    
    def delete(self, id: int) -> bool:
        validate_id(id)
        return self.transaction.delete(id)

    def category_add(self, name: str) -> None:
        name = validate_category_name(name)

        if self.category_exists(name): raise ValueError(f"이미 등록된 카테고리입니다: {name}")
        self.category.save({"name": name})
        
    def category_list(self) -> list[dict]:
        return list(self.category.stream())

    def category_remove(self, name: str) -> bool:
        name = validate_category_name(name)

        if not self.category_exists(name): return False

        for data in self.transaction.stream():
            if data["category"] == name:
                raise ValueError(f"사용중인 카테고리는 삭제할 수 없습니다: {name}")

        category = [
            data
            for data in self.category.stream()
            if  data["name"] != name
        ]

        self.category.rewrite(category)
        return True

    def budget_set(self, month: str, amount: int) -> None:
        validate_month(month)
        validate_amount(amount)

        data = list(self.budget.stream())

        for item in data:
            if  item["month"] == month:
                item["amount"] = amount
                self.budget.rewrite(data)
                return

        data.append({
            "month" : month,
            "amount": amount
        })

        self.budget.rewrite(data)

    def summary(self, month: str, top: int = 3) -> dict:
        validate_month(month)
        validate_top(top)

        total_income   = 0
        total_expense  = 0
        category_total = defaultdict(int)

        for data in self.transaction.stream():
            if   not data["date"].startswith(month): continue
            if   data["type"] == "income"          : total_income += data["amount"]
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

        budget_usage = 0
        if budget_amount > 0: budget_usage = round(total_expense / budget_amount * 100, 2)

        return {
            "month"          : month,
            "total_income"   : total_income,
            "total_expense"  : total_expense,
            "balance"        : total_income - total_expense,
            "budget"         : budget_amount,
            "top_categories" : top_categories,
            "budget_usage"   : budget_usage,
            "budget_exceeded": (budget_amount > 0 and total_expense > budget_amount)
        }

    def search(self, date_from: str | None = None, date_to: str | None = None,
                     category : str | None = None, type   : str | None = None, 
                     q        : str | None = None, tag    : str | None = None
            ) -> list[dict]:
        validate_date_range(date_from, date_to)
        if category is not None: validate_category_name(category)
        if type     is not None: validate_type(type)

        data_list = []

        for data in self.transaction.stream():
            if date_from is not None and data["date"]      < date_from: continue
            if date_to   is not None and data["date"]      > date_to  : continue
            if category  is not None and data["category"] != category : continue
            if type      is not None and data["type"]     != type     : continue
            if q         is not None and q   not in data["memo"]      : continue
            if tag       is not None and tag not in data["tags"]      : continue

            data_list.append(data)
        data_list.sort(key=lambda item: item["date"], reverse=True)

        return data_list

    def import_csv(self, file_path: str) -> int:
        validate_csv_file(file_path)
        data_list = self.transaction.import_csv(file_path)

        for data in data_list:
            validate_date(data["date"])
            validate_amount(data["amount"])
            validate_type(data["type"])
            validate_category_name(data["category"])
            validate_memo(data["memo"])
            validate_tags(data["tags"])
            self.validate_transaction_category(data["category"])

        for data in data_list:
            data["id"] = self.next_id()
            self.add(Transaction(**data))

        return len(data_list)

    def export_csv(self, file_path: str,         month  : str | None = None,
                   date_from: str | None = None, date_to: str | None = None
        ) -> int:
        validate_csv_file(file_path)
        validate_export_condition(month, date_from, date_to)

        data_list = []

        for data in self.transaction.stream():
            if month     is not None and not data["date"].startswith(month) : continue
            if date_from is not None and     data["date"] < date_from       : continue
            if date_to   is not None and     data["date"] > date_to         : continue

            data_list.append(data)

        self.transaction.export_csv(file_path, data_list)
        return len(data_list)