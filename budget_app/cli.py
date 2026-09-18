import argparse

def create_parser() -> argparse.ArgumentParser:
    parser   = argparse.ArgumentParser()
    subparse = parser.add_subparsers(dest="command", required=True)

    subparse.add_parser("add")

    list = subparse.add_parser("list")
    list.add_argument("--limit", type=int)

    detail = subparse.add_parser("detail")
    detail.add_argument("id", type=int)

    update = subparse.add_parser("update")
    update.add_argument("id", type=int)

    delete = subparse.add_parser("delete")
    delete.add_argument("id", type=int)

    category     = subparse.add_parser("category")
    category_sub = category.add_subparsers(dest="cate", required=True)
    category_sub.add_parser("list")

    category_add = category_sub.add_parser("add")
    category_add.add_argument("name")

    category_rmv = category_sub.add_parser("remove")
    category_rmv.add_argument("name")

    budget     = subparse.add_parser("budget")
    budget_add = budget.add_subparsers(dest="budget", required=True)
    budget_set = budget_add.add_parser("set")
    budget_set.add_argument("--month",  required=True)
    budget_set.add_argument("--amount", required=True, type=int)

    summary = subparse.add_parser("summary")
    summary.add_argument("--month", required=True)
    summary.add_argument("--top", type=int, default=3)

    search = subparse.add_parser("search")
    search.add_argument("--from", dest="date_from")
    search.add_argument("--to"  , dest="date_to")
    search.add_argument("--category")
    search.add_argument("--type")
    search.add_argument("--q")
    search.add_argument("--tag")

    import_cmd = subparse.add_parser("import")
    import_cmd.add_argument("--from", dest="file", required=True)

    export_cmd = subparse.add_parser("export")
    export_cmd.add_argument("--out" , required=True)
    export_cmd.add_argument("--month")
    export_cmd.add_argument("--from", dest="date_from")
    export_cmd.add_argument("--to"  , dest="date_to")

    return parser