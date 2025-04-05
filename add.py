import argparse
import pathlib
import sys
from bs4 import BeautifulSoup
from bs4 import Comment
import re


class Add:
    @staticmethod
    def add(args: argparse.Namespace) -> None:
        """
        Entry point for the functionality of the 'add' command
        """
        fin, flashcard_type = Add._get_clean_user_input(args)

        Add.modify_html(fin, flashcard_type)

    @staticmethod
    def _get_clean_user_input(args) -> tuple[pathlib.Path, str]:
        """
        Returns a tuple containing the path to the input file and a string
        indicating the kind of flashcards to be added. If there is an error,
        print info to the user and stop the program.
        """
        error: bool = False

        if not (args.cloze or args.basic):
            print(
                "ERROR: use '-c' or '-b' to indicate the type of "
                + "flashcard to add"
            )
            error = True

        if args.cloze and args.basic:
            print("ERROR: use only one flag.")
            error = True

        fin_path = pathlib.Path(args.input)
        if not fin_path.exists():
            print(f"ERROR: file '{fin_path}' doesn't exist.")
            error = True

        if error:
            sys.exit()

        flashcard_type: str
        if args.cloze:
            flashcard_type = "cloze"
        else:
            flashcard_type = "basic"

        return fin_path, flashcard_type

    @staticmethod
    def _get_next_cardnumber(html: BeautifulSoup) -> int:
        """
        Return the card number for the h2.cardnumber element to be created.
        """
        cardnumber_elements: list[str] = html.find_all(
            attrs={"class": "cardnumber"}
        )

        if not cardnumber_elements:
            return 1

        cardnumber_element = BeautifulSoup(
            str(cardnumber_elements[-1]), "html.parser"
        )

        match = re.match(
            r"[^\d]*(\d{1,}).*", cardnumber_element.get_text().strip()
        )

        cardnumber = match.group(1)
        return int(cardnumber) + 1

    @staticmethod
    def _append_new_h2_cardnumber(
        new_cardnumber: int, html_doc: BeautifulSoup
    ) -> None:
        new_cardnumber_element = html_doc.new_tag(
            "h1", attrs={"class": "cardnumber"}
        )
        new_cardnumber_element.string = "Card " + str(new_cardnumber)

        # add card number header element
        try:
            html_doc.html.body.append(new_cardnumber_element)
        except AttributeError:
            print("ERROR: There is no html document inside the file input!")
            sys.exit()

    @staticmethod
    def _append_div_flashcardcloze(html_doc: BeautifulSoup) -> None:
        flashcard_element = html_doc.new_tag(
            "div", attrs={"class": "flashcardcloze"}
        )

        # add flashcard div element
        html_doc.html.body.append(flashcard_element)

    @staticmethod
    def _append_div_flashcardbasic(html_doc: BeautifulSoup) -> None:
        # create flashcard div element
        flashcard_element = html_doc.new_tag(
            "div", attrs={"class": "flashcard"}
        )

        # create hr.frontback element
        hr_frontback_element = html_doc.new_tag(
            "hr", attrs={"class": "frontback"}
        )

        # append hr.frontback element to flashcard div element
        flashcard_element.append(hr_frontback_element)

        # add flashcard div element
        html_doc.html.body.append(flashcard_element)

    @staticmethod
    def _append_comment(html_doc: BeautifulSoup) -> None:
        html_doc.html.body.append(Comment(f' {"-" * 66} '))

    @staticmethod
    def modify_html(input_path: pathlib.Path, flashcard_type: str) -> None:
        # TODO refactor this function
        with open(input_path, "r") as f:
            lines = f.readlines()

        HTML_DOC = ""
        for line in lines:
            HTML_DOC += line

        main_html_doc: BeautifulSoup = BeautifulSoup(HTML_DOC, "html.parser")

        new_cardnumber = Add._get_next_cardnumber(main_html_doc)

        Add._append_new_h2_cardnumber(new_cardnumber, main_html_doc)

        if flashcard_type == "cloze":
            Add._append_div_flashcardcloze(main_html_doc)
        else:
            Add._append_div_flashcardbasic(main_html_doc)

        Add._append_comment(main_html_doc)

        with open(input_path, "w") as f:
            f.write(main_html_doc.prettify())
