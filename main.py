import sys

from args import get_args

# CONSTANTS
DEFAULT_TEMPLATE_FILE_NAME = "html2anki_template.html"


def main():
    args = get_args().parse_args()
    print(args)
    sys.exit()

    # TEMPLATE ----------------------------------------------------------------
    if args.subcommand == "template":
        if not args.output:
            template_filename: str = DEFAULT_TEMPLATE_FILE_NAME
        else:
            template_filename: str = args.output

        print(f"TEMPLATE subcommand. Output file: '{template_filename}'")

    # CONVERT -----------------------------------------------------------------
    elif args.subcommand == "convert":
        if args.tag:
            tag_name: str = args.tag
        else:
            tag_name: str = args.input_file.replace(".html", "")

        if not args.output:
            csv_filename: str = f"{args.input_file.replace('.html', '.csv')}"
        else:
            csv_filename = args.output

        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"

        print("CONVERT subcommand")
        print(f"input file: '{args.input_file}'")
        print(f"output file: '{csv_filename}'")
        print(f"tag: '{tag_name}'")

    else:
        print("")
        parent_parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
