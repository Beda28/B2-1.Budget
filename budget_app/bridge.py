from .model   import Transaction
from .service import TransactionService

def bridge(args) -> None:
    service = TransactionService()

    if args.command == "add":
        data = Transaction(
            id       = int(service.next_id()),
            type     = input("거래 타입(income/expense): "),
            date     = input("거래 날짜(YYYY-MM-DD): "),
            amount   = int(input("거래 금액: ")),
            category = input("카테고리: "),
            memo     = input("메모: "),
            tags     = split_tag()
        )

        service.add(data)
        print("거래가 추가되었습니다.")

    elif args.command == "list":
        datas = service.list(args.limit)

        if not datas: return print("거래 내역이 없습니다.")
        print("ID  날짜       타입          금액    카테고리")

        for data in datas:
            print(
                f"{data['id']:<3} "
                f"{data['date']} "
                f"{data['type']:<10} "
                f"{data['amount']:>8}원 "
                f"{data['category']}"
            )

    elif args.command == 'detail':
        data = service.detail(args.id)

        if data is None: return print("해당 거래를 찾을 수 없습니다.")

        print(f"거래 ID  : {data['id']}")
        print(f"거래 타입: {data['type']}")
        print(f"거래 날짜: {data['date']}")
        print(f"거래 금액: {data['amount']}원")
        print(f"카테고리 : {data['category']}")
        print(f"메모: {data['memo']}")
        print(f"태그: {', '.join(data['tags'])}")

    elif args.command == 'update':
        data = service.detail(args.id)

        if data is None: return print("해당 거래를 찾을 수 없습니다.")

        print ("Enter를 누르면 기존 값으로 유지됩니다.")
        update_data = Transaction(
            id       = args.id,
            type     = input("거래 타입(income/expense): ") or data["type"],
            date     = input("거래 날짜(YYYY-MM-DD): ")     or data["date"],
            amount   = int(input("거래 금액: ")             or data["amount"]),
            category = input("카테고리: ")                  or data["category"],
            memo     = input("메모: ")                      or data["memo"],
            tags     = split_tag()
        )

        service.update(args.id, update_data)
        print("거래가 수정되었습니다.")

def split_tag() -> list[str]:
    tag = input("태그: ")
    tag.strip()
    return tag.split(",")