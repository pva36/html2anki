import argparse
import pathlib
import sys
from bs4 import BeautifulSoup


class Template:
    @staticmethod
    def template(args: argparse.Namespace) -> None:
        """
        Entry point for the functionality of the 'template' command
        """
        output_path = Template._get_clean_user_input(args)
        Template._create_html_template(output_path)

    @staticmethod
    def _create_html_template(html_template_path: pathlib.Path) -> None:
        """
        Create an html containing the template structure of the type of html
        file the program handles.
        """

        html_template = (
            "<!DOCTYPE html>"
            '<html lang="en">\n'
            "   <head>\n"
            '       <meta charset="UTF-8">\n'
            "       <meta\n"
            '           name="viewport"\n'
            '           content="width=device-width, initial-scale=1">\n'
            "       <title></title>\n"
            "       <style>\n"
            "   body {\n"
            "       text-align: center;\n"
            "   }\n"
            "   .flashcard, .flashcardcloze {\n"
            "       border-style: solid;\n"
            "       border-radius: 5px;\n"
            "       margin-bottom: 20px;\n"
            "       padding: 10px;\n"
            "   }\n"
            "   .frontback {\n"
            "       size: 5px;\n"
            "   }\n"
            "   . cardnumber {\n"
            "       background-color: blue;\n"
            "   }\n"
            "        </style>\n"
            "    </head>\n"
            "    <body>\n"
            "    </body>\n"
            "</html>"
        )
        html_doc = BeautifulSoup(html_template, "html.parser")
        with open(html_template_path, "w") as file:
            file.write(html_doc.prettify())
        print(f'The file "{html_template_path}" has been created.')

    @staticmethod
    def _get_clean_user_input(args: argparse.Namespace) -> pathlib.Path:
        """
        Returns a pathlib.Path object containing the path to the output file
        If output file already exists, send an error message to the user and
        exit the program.
        """
        output_path: pathlib.Path

        if args.output:
            output_path = pathlib.Path(args.output)
        else:
            output_path = pathlib.Path("html2anki_template.html")

        if output_path.exists():
            print(f"ERROR: Output file '{output_path}' already exists.")
            sys.exit()
        else:
            return output_path
