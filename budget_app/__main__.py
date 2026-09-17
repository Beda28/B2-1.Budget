from .cli     import create_parser
from .bridge  import bridge

if __name__ == "__main__":
    parser = create_parser()
    args   = parser.parse_args()

    bridge(args=args)