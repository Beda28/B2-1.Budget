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

    return parser