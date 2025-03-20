import argparse
import pathlib
import sys
import re
import csv
from bs4 import BeautifulSoup
from bs4 import Comment

import functions as f


class Convert:
    @staticmethod
    def convert(args: argparse.Namespace) -> None:
        """
        Entry point for the functionality of the 'convert' command
        """
        fin_path, fout_prefix, tag = Convert._get_clean_user_input(args)

        # create the BeautifulSoup object containing the input html
        with open(fin_path, "r") as f:
            html_lines = f.readlines()

        html_doc_str: str = ""
        for line in html_lines:
            html_doc_str += line

        main_html_doc: BeautifulSoup = BeautifulSoup(
            html_doc_str,
            "html.parser",
        )

        # remove comments
        comments = main_html_doc.find_all(
            string=lambda text: isinstance(text, Comment)
        )

        for comment in comments:
            comment.extract()

        # extract all flashcards from document
        flashcards_basic_raw: list[str] = Convert._get_raw_flashcards(
            main_html_doc, "flashcard"
        )
        flashcards_cloze_raw: list[str] = Convert._get_raw_flashcards(
            main_html_doc, "flashcardcloze"
        )

        # store the cleaned and ready to save flashcards
        basic_flashcards: list[str] = []
        cloze_flashcards: list[str] = []
        for s in flashcards_basic_raw:
            basic_flashcards.append(Convert._format_flashcard(s))
        for s in flashcards_cloze_raw:
            cloze_flashcards.append(Convert._format_flashcard(s))

        if (len(basic_flashcards) == 0) and (len(cloze_flashcards) == 0):
            print("ERROR: The input file does not contain any flashcards!")
            sys.exit()
        if len(basic_flashcards) > 0:
            Convert._write_basic_flashcards(basic_flashcards, fout_prefix, tag)

        if len(cloze_flashcards) > 0:
            Convert._write_cloze_flashcards(cloze_flashcards, fout_prefix, tag)

    @staticmethod
    def _split_basic_flashcards(
        basic_flashcards: list[str],
    ) -> list[tuple[str, str]]:
        tuples: list[tuple[str, str]] = []
        for flashcard in basic_flashcards:
            back_segment: bool = False
            front: str = ""
            back: str = ""
            lines = flashcard.split("\n")
            for line in lines:
                if '<hr class="frontback"' in line:
                    back_segment = True
                    continue
                if not back_segment:
                    front += line + "\n"
                else:
                    back += line + "\n"
            tuples.append((front.rstrip(), back.rstrip()))

        return tuples

    @staticmethod
    def _write_basic_flashcards(
        basic_flashcards: list[str], fout_prefix: str, tag: str
    ) -> None:
        out_path = pathlib.Path(fout_prefix + "_basic.tsv")
        basic_flashcards_t = Convert._split_basic_flashcards(basic_flashcards)

        with open(out_path, "w", newline="") as tsvfile:
            writer = csv.writer(tsvfile, delimiter="\t")
            for tuple in basic_flashcards_t:
                writer.writerow([tuple[0], tuple[1], tag])

        print(f"The file '{out_path}' has been successfully written.")

    @staticmethod
    def _write_cloze_flashcards(
        cloze_flashcards: list[str], fout_prefix: str, tag: str
    ) -> None:
        out_path = pathlib.Path(fout_prefix + "_cloze.tsv")

        with open(out_path, "w", newline="") as tsvfile:
            writer = csv.writer(tsvfile, delimiter="\t")
            for flashcard in cloze_flashcards:
                writer.writerow([flashcard, tag])

        print(f"The File '{out_path}' has been successfully written.")

    @staticmethod
    def _get_raw_flashcards(
        html_doc: BeautifulSoup, flashcard_class: str
    ) -> list[str]:
        flashcard_elements = html_doc.find_all(
            name="div", attrs={"class": flashcard_class}
        )
        flashcard_raw: list[str] = []

        first_tag_regex: str = ""
        if flashcard_class == "flashcardcloze":
            first_tag_regex = r"^<div class=\"flashcardcloze\">"
        else:
            first_tag_regex = r"^<div class=\"flashcard\">"

        # remove the div flashcard tags
        for elem in flashcard_elements:
            elem_str = re.sub(first_tag_regex, "", str(elem))
            elem_str = re.sub(r"</div>$", "", elem_str)
            flashcard_raw.append(elem_str.strip())

        return flashcard_raw

    @staticmethod
    def _get_all_pre_content(flashcard: str) -> list[str]:
        """
        Extract every line inside any pre block in the flashcard. Returns those
        as a list of string, where each string is a line inside the pre block.
        """
        pre_blocks_raw = BeautifulSoup(flashcard, "html.parser").find_all(
            "pre"
        )

        pre_blocks_clean: list[str] = []

        for block in pre_blocks_raw:
            if match := re.match(r"<\s*pre.*>([\s\S]*)<.*/pre.*>", str(block)):
                pre_blocks_clean.append(match.group(1).strip())

        # contains all the lines inside any pre element
        pre_content: list[str] = []

        for s in pre_blocks_clean:
            pre_lines = s.split("\n")
            for line in pre_lines:
                pre_content.append(line)

        return pre_content

    @staticmethod
    def _not_a_pre_line(line: str, pre_lines: list[str]) -> bool:
        if len(pre_lines) == 0:
            return True
        for pre_line in pre_lines:
            if pre_line == line:
                return False
        return True

    @staticmethod
    def _format_flashcard(flashcard: str) -> str:
        # check if flashcard contains pre html elements

        pre_content: list[str] = []

        has_pre_regex = r"^[\s\S]*<\s*pre.*>([\s\S]*)<.*/pre.*>[\s\S]*$"
        if re.match(has_pre_regex, flashcard):
            pre_content = Convert._get_all_pre_content(flashcard)

        lines = flashcard.split("\n")

        formated_lines: list[str] = []

        for line in lines:
            if not Convert._not_a_pre_line(line, pre_content):
                formated_lines.append(line)
            else:
                formated_line = re.sub(r"^\s*", "", line)
                formated_lines.append(formated_line)

        flashcard_cleaned = ""
        for line in formated_lines:
            flashcard_cleaned += line + "\n"

        flashcard_cleaned = flashcard_cleaned.rstrip()

        soup = BeautifulSoup(flashcard_cleaned, "html.parser")

        return soup.prettify().strip()

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
