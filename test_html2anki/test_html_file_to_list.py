import sys

sys.path.append("..")

from html2anki import (
    html_file_to_list,
    strip_list_of_flashcards,
    list_to_basic_n_cloze,
    create_html_template,
)


def main():
    print("html_file_to_list(file_path)")
    list_of_flashcards = html_file_to_list("test_html_file_to_list.html")
    for flashcard in list_of_flashcards:
        print("\n")
        for line in flashcard:
            print(f'"{line}"')
    print("\n")

    print("stripped_list_of_flashcards(list_of_flashcards, br_switch)")
    list_of_flashcards_stripped = strip_list_of_flashcards(
        list_of_flashcards, True
    )
    for flashcard in list_of_flashcards_stripped:
        print("\n")
        for line in flashcard:
            print(f'"{line}"')

    print("list_to_basic_n_cloze(list_of_flashcards)")
    list_of_basic, list_of_cloze = list_to_basic_n_cloze(
        list_of_flashcards_stripped
    )

    print("\nBASIC:\n")
    for flashcard in list_of_basic:
        print(flashcard)

    print("\nCLOZE:\n")
    for flashcard in list_of_cloze:
        print(flashcard)

    create_html_template("template.html")


if __name__ == "__main__":
    main()
