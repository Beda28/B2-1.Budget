import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="budget_app", description="나만의 용돈 기입장")
    parser.add_argument("--data-dir", default="./data", help="데이터 저장 폴더" )

    subparsers  = parser.add_subparsers(dest="command", required=True)

    add_parser  = subparsers.add_parser("add", help="거래 추가" )

    list_parser = subparsers.add_parser("list", help="거래 목록 조회" )
    list_parser.add_argument("--limit", type=int, default=10, help="조회할 거래 수")

    search_parser = subparsers.add_parser("search", help="거래 검색")
    search_parser.add_argument("--from",     dest="from_date", help="검색 시작일 YYYY-MM-DD")
    search_parser.add_argument("--to",       dest="to_date",   help="검색 종료일 YYYY-MM-DD")
    search_parser.add_argument("--category", help="카테고리")
    search_parser.add_argument("--type",     choices=["income", "expense"], help="거래 타입")
    search_parser.add_argument("--q",        help="메모 검색어")
    search_parser.add_argument("--tag",      help="태그")

    summary_parser = subparsers.add_parser("summary",           help="월별 요약")
    summary_parser.add_argument("--month", required=True,       help="조회 월 YYYY-MM")
    summary_parser.add_argument("--top",   type=int, default=3, help="지출 TOP N")

    budget_parser     = subparsers   .add_parser("budget", help="예산 관리")
    budget_subparsers = budget_parser.add_subparsers(dest="budget_command",required=True)

    budget_set_parser = budget_subparsers.add_parser("set", help="월 예산 설정")
    budget_set_parser.add_argument("--month",  required=True, help="예산 월 YYYY-MM")
    budget_set_parser.add_argument("--amount", required=True, type=int, help="예산 금액")

    budget_subparsers.add_parser("list", help="예산 목록 조회")

    category_parser     = subparsers     .add_parser("category", help="카테고리 관리")
    category_subparsers = category_parser.add_subparsers(dest="category_command", required=True)

    category_add_parser = category_subparsers.add_parser("add", help="카테고리 추가")
    category_add_parser.add_argument("--name", help="카테고리명")
    category_subparsers.add_parser("list", help="카테고리 목록 조회")
    category_remove_parser = category_subparsers.add_parser("remove", help="카테고리 삭제")
    category_remove_parser.add_argument("--name", help="카테고리명")

    update_parser = subparsers.add_parser("update", help="거래 수정")
    update_parser.add_argument("--id",       required=True, help="수정할 거래 ID")
    update_parser.add_argument("--date",     help="날짜 YYYY-MM-DD")
    update_parser.add_argument("--type",     choices=["income", "expense"], help="거래 타입")
    update_parser.add_argument("--category", help="카테고리")
    update_parser.add_argument("--amount",   type=int, help="금액")
    update_parser.add_argument("--memo",     help="메모")
    update_parser.add_argument("--tags",     help="태그, 쉼표 구분")

    delete_parser = subparsers.add_parser("delete", help="거래 삭제")
    delete_parser.add_argument("--id", required=True, help="삭제할 거래 ID")

    import_parser = subparsers.add_parser("import", help="CSV 거래 가져오기")
    import_parser.add_argument("--from", dest="from_file", required=True, help="가져올 CSV 파일")

    export_parser = subparsers.add_parser("export", help="CSV 거래 내보내기")
    export_parser.add_argument("--out", required=True, help="출력 CSV 파일")
    export_parser.add_argument("--month", help="내보낼 월 YYYY-MM")
    export_parser.add_argument("--from", dest="from_date", help="검색 시작일 YYYY-MM-DD")
    export_parser.add_argument("--to", dest="to_date", help="검색 종료일 YYYY-MM-DD")

    return parser