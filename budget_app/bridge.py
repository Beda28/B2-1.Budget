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

    if args.command == "list":
        transaction = service.list(args.limit)

        if not transaction: return print("거래 내역이 없습니다.")
        print("ID  날짜       타입          금액    카테고리")

        for transactions in transaction:
            print(
                f"{transactions['id']:<3} "
                f"{transactions['date']} "
                f"{transactions['type']:<10} "
                f"{transactions['amount']:>8}원 "
                f"{transactions['category']}"
            )

    if args.command == 'detail':
        transaction = service.detail(args.id)

        if transaction is None: return print("해당 거래를 찾을 수 없습니다.")

        print(f"거래 ID  : {transaction['id']}")
        print(f"거래 타입: {transaction['type']}")
        print(f"거래 날짜: {transaction['date']}")
        print(f"거래 금액: {transaction['amount']}원")
        print(f"카테고리 : {transaction['category']}")
        print(f"메모: {transaction['memo']}")
        print(f"태그: {', '.join(transaction['tags'])}")