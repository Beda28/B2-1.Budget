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
            memo     = input("메모: ")                      or data["memo"]
        )

        tags     = split_tag()
        if tags != []: update_data.tags = tags

        service.update(args.id, update_data)
        print("거래가 수정되었습니다.")

    elif args.command == 'delete':
        if service.delete(args.id) : print("거래가 삭제되었습니다.")
        else                       : print("거래를 찾을 수 없습니다.")

    elif args.command == 'category':
        if args.cate  == "add":
            service.category_add(args.name)
            print("카테고리가 추가되었습니다.")
        elif args.cate == "list":
            category = service.category_list()

            if not category: return print("카테고리가 없습니다.")
            for cate in category:   print(cate["name"])

        elif args.cate == "remove":
            if service.category_remove(args.name): print("카테고리가 삭제되었습니다.")
            else                                 : print("카테고리를 찾을 수 없습니다.")

    elif args.command == 'budget':
        if args.budget == 'set':
            service.budget_set(args.month, args.amount)
            print("예산이 설정되었습니다.")

    elif args.command == 'summary':
        data = service.summary(args.month, args.top)

        if data["total_income"] == 0 and data['total_expense'] == 0:
            return print("해당 월의 거래 내역이 없습니다.")
        
        print(f"{data['month']} 요약")
        print()
        print(f"총수입: {data['total_income']}원")
        print(f"총지출: {data['total_expense']}원")
        print(f"잔액: {data['balance']}원")

        if data["budget"] > 0:
            print()
            print(f"예산: {data['budget']}원")
            print(f"예산 사용액: {data['total_expense']}원")
            print(f"예산 사용률: {data['budget_usage']:.1f}%")

            if data['budget_exceeded']:
                print(f"예산 초과: {data['total_expense'] - data['budget']}원")

        print()
        print(f"지출 TOP {args.top}")

        if not data["top_categories"]:
            print("지출 내역이 없습니다.")

        for category, amount in data["top_categories"]:
            print(f"{category}: {amount}원")

    elif args.command == 'search':
        datas = service.search(
            date_from = args.date_from,
            date_to   = args.date_to,
            category  = args.category,
            type      = args.type,
            q         = args.q,
            tag       = args.tag
        )

        if not datas: return print("검색 결과가 없습니다.")
        print("ID  날짜       타입          금액    카테고리")

        for data in datas:
            print(
                f"{data['id']:<3} "
                f"{data['date']} "
                f"{data['type']:<10} "
                f"{data['amount']:>8}원 "
                f"{data['category']}"
            )

    elif args.command == 'import':
        count = service.import_csv(args.file)
        print(f"{count}개의 거래를 가져왔습니다.")

    elif args.command == 'export':
        if not args.month and not args.date_from and not args.date_to:
            return print("month 또는 from/to 조건이 필요합니다.")

        count = service.export_csv(
            file_path = args.out,
            month     = args.month,
            date_from = args.date_from,
            date_to   = args.date_to
        )

        print(f"{count}개의 거래를 내보냈습니다.")

def split_tag() -> list[str]:
    tag = input("태그: ").strip()
    if not tag: return []
    return tag.split(",")