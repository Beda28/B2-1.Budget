import argparse

def create_parser() -> argparse.ArgumentParser:
    parser   = argparse.ArgumentParser()
    subparse = parser.add_subparsers(dest="command", required=True)

    subparse.add_parser("add")
    subparse.add_parser("list")

    detail = subparse.add_parser("detail")
    detail.add_argument("id", type=int)

    return parser