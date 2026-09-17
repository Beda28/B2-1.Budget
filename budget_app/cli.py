import argparse

def create_parser() -> argparse.ArgumentParser:
    parser   = argparse.ArgumentParser()
    subparse = parser.add_subparsers(dest="command", required=True)

    subparse.add_parser("add")
    subparse.add_parser("list")

    return parser