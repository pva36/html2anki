import argparse


def get_args() -> argparse.ArgumentParser:
    parent_parser = argparse.ArgumentParser(prog="html2anki")

    subparsers = parent_parser.add_subparsers(
        title="subcommands", dest="subcommand"
    )

    add_convert_parser(subparsers)
    add_template_parser(subparsers)

    return parent_parser


def add_convert_parser(subparsers: argparse._SubParsersAction) -> None:
    # TODO add description into add_parser
    parser_convert = subparsers.add_parser("convert")
    parser_convert.add_argument("--input-file", "-i", type=str, required=True)
    parser_convert.add_argument(
        "--output-files-prefix",
        "-op",
        type=str,
        help="output files' prefix. By default, the name of the input file"
        + " without the file extension.",
    )
    parser_convert.add_argument(
        "--tag",
        "-t",
        type=str,
        help="flashcards' tag. By default, the name "
        + "of the input file without the file extension.",
    )


def add_template_parser(subparsers: argparse._SubParsersAction) -> None:
    # TODO add description into add_parser
    parser_template = subparsers.add_parser("template")
    parser_template.add_argument(
        "-o",
        "--output",
        help="Prefix of the file to be created. By default"
        + "'html2anki_template.html'",
        type=str,
        required=True,
    )
