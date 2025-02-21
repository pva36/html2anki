import argparse
import pathlib
import sys

import functions as f


class Convert:
    @staticmethod
    def convert(args: argparse.Namespace) -> None:
        """
        Entry point for the functionality of the 'convert' command
        """
        fin_path, fout_prefix, tag = Convert._get_clean_user_input(args)

    @staticmethod
    def _get_clean_user_input(
        args: argparse.Namespace,
    ) -> tuple[pathlib.Path, str, str]:
        """
        Returns a tuple containing a path to the entry
        """
        # check input file
        input_file: pathlib.Path = pathlib.Path(args.input_file)
        if not input_file.exists():
            print(f"Error: Input file '{args.input_file}' doesn't exist.")
            sys.exit()

        # check output file
        output_file_prefix: str
        out_file_exists = f.out_files_exists(
            args.output_files_prefix, input_file
        )
        if out_file_exists[0]:
            print(out_file_exists[1])
            sys.exit()
        else:
            if args.output_files_prefix:
                output_file_prefix = args.output_files_prefix
            else:
                output_file_prefix, _ = input_file.name.split(".")

        # check tag
        tag: str
        if args.tag:
            tag = args.tag
        else:
            tag, _ = input_file.name.split(".")

        return (input_file, output_file_prefix, tag)
