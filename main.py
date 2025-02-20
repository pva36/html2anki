import sys

from args import get_args
from convert import Convert
from template import Template


def main() -> None:
    args = get_args().parse_args()

    if args.subcommand == "convert":
        Convert.convert(args)

    elif args.subcommand == "template":
        Template.template(args)

    else:
        get_args().parse_args(["--help"])
        sys.exit()


if __name__ == "__main__":
    main()
