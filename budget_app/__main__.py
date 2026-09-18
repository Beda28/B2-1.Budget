from .cli       import create_parser
from .bridge    import bridge
from .decorator import handle_error

@handle_error
def main():
    parser = create_parser()
    args   = parser.parse_args()

    bridge(args=args)
    
if __name__ == "__main__":
    main()