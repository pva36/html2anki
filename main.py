import argparse

# CONSTANTS
DEFAULT_TEMPLATE_FILE_NAME = "html2anki_template.html"


def main():
    # argsparse stuff ---------------------------------------------------------
    parent_parser = argparse.ArgumentParser(prog="html2anki")

    # 'dest' option is a placeholder in Namespace Object returned by
    # 'argparse.ArgumentParser().parse_args()'. This allows to check whether
    # a subcommand was entered (and which one exactly)
    subparsers = parent_parser.add_subparsers(
        title="subcommands",
        dest="subcommand",
    )

    # CONVERT parser
    parser_convert = subparsers.add_parser("convert")
    parser_convert.add_argument("input_file", type=str)
    parser_convert.add_argument(
        "-o", "--output", help="Output file's name.", type=str
    )
    parser_convert.add_argument(
        "-t", "--tag", help="Flashcard's tag.", type=str
    )

    # TEMPLATE parser
    parser_template = subparsers.add_parser("template")
    parser_template.add_argument(
        "-o",
        "--output",
        help="Name of the file to be created. By default "
        + f"'{DEFAULT_TEMPLATE_FILE_NAME}'.",
        type=str,
    )

    args = parent_parser.parse_args()  # contains all the arguments

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
