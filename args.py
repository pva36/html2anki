import argparse


def get_args() -> argparse.ArgumentParser:
    program_description = "Converts custom html files into anki flashcards."
    epilog_msg = "Use 'html2anki {subcommand} --help' to get detailed info "
    epilog_msg += "per subcommand"
    parent_parser = argparse.ArgumentParser(
        prog="html2anki", description=program_description, epilog=epilog_msg
    )

    subparsers = parent_parser.add_subparsers(
        title="subcommands", dest="subcommand"
    )

    add_convert_parser(subparsers)
    add_template_parser(subparsers)
    add_add_parser(subparsers)

    return parent_parser


def add_convert_parser(subparsers: argparse._SubParsersAction) -> None:
    description = "Extract all div elements of class 'flashcard' or "
    description += "'flashcardcloze' and create tsv files containing them, "
    description += "ready to import into anki (one per file)"
    parser_convert = subparsers.add_parser("convert", description=description)
    parser_convert.add_argument("-i", "--input-file", type=str, required=True)

    parser_convert.add_argument(
        "-op",
        "--output-files-prefix",
        type=str,
        help="default value: the name of the input file"
        + " without the file extension.",
    )

    parser_convert.add_argument(
        "-t",
        "--tag",
        type=str,
        help="default value: the name "
        + "of the input file without the file extension.",
    )


def add_template_parser(subparsers: argparse._SubParsersAction) -> None:
    description = "creates an empty html document"

    parser_template = subparsers.add_parser(
        "template", description=description
    )

    parser_template.add_argument(
        "-o",
        "--output",
        help="name of the file to be created. Default value: "
        + "'html2anki_template.html'",
        type=str,
    )


def add_add_parser(subparsers: argparse._SubParsersAction) -> None:
    description = "appends an empty html div element of class 'flashcard' or "
    description += "'flashcardcloze' as the last child element of the body of "
    description += "the INPUT_FILE's html document "
    add_usage = "html2anki add [-h] [Exactly one of : -c, -b] input"

    parser_add = subparsers.add_parser(
        "add", usage=add_usage, description=description
    )

    parser_add.add_argument("input", type=str)
    parser_add.add_argument("-c", "--cloze", action="store_true")
    parser_add.add_argument("-b", "--basic", action="store_true")
