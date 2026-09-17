from uuid    import uuid4
from model   import Transaction
from service import TransactionService

def bridge(args) -> None:
    service = TransactionService()

    if args.command == "add":
        transaction = Transaction(
            id       = int(service.next_id()),
            type     = input("거래 타입(income/expense): "),
            date     = input("거래 날짜(YYYY-MM-DD): "),
            amount   = int(input("거래 금액: ")),
            category = input("카테고리: "),
            memo     = input("메모: "),
            tags     = input("태그: ").split(",")
        )

        service.add(transaction)
        print("거래가 추가되었습니다.")