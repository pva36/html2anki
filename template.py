import argparse
import pathlib
import sys


class Template:
    @staticmethod
    def template(args: argparse.Namespace) -> None:
        """
        Entry point for the functionality of the 'template' command
        """
        output_path = Template._get_clean_user_input(args)

    @staticmethod
    def _get_clean_user_input(args: argparse.Namespace) -> pathlib.Path:
        """
        Returns a pathlib.Path object containing the path to the output file
        If output file already exists, send an error message to the user and
        exit the program.
        """
        output_path = pathlib.Path(args.output)

        if output_path.exists():
            print(f"ERROR: Output file '{output_path}' already exists.")
            sys.exit()
        else:
            return output_path
