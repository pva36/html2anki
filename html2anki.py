#!/usr/bin/python3

# html2anki

# Main program
import sys
import os


# main function
def main():

    # default values
    # br_line_in_pre_element = True

    # Process Command line arguments
    if len(sys.argv) == 1:
        print("No command was entered. Enter \"html2anki -h\" for help")
        sys.exit()

    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(help_message())
        sys.exit()

    elif (sys.argv[1] == "template") or (sys.argv[1] == 't'):
        counter = 1
        html_template = None
        skip_template = False

        for argument in sys.argv[2:]:
            counter += 1
            if skip_template is True:
                skip_template = False
                continue

            if ("-f" in argument) or ("--file" in argument):
                skip_template = True
                html_template = sys.argv[counter + 1].strip()

                if html_template.endswith('.html') is False:
                    print('The filename indicated doesn\'t have an ".html" '
                          'suffix.')
                    sys.exit()

                elif os.path.isfile(f".//{html_template}") is True:
                    print(f'The file "{html_template}" already exists in the '
                          'current directory.')
                    sys.exit()

            else:
                print(f'WARNING:\t"{argument}" is not a valid option for'
                      ' template.')
                sys.exit()

        if html_template is None:
            html_template = "html2anki_template.html"
            if os.path.isfile(html_template) is True:
                print(f'A file with the default name "{html_template}" already'
                      ' exists in the current directory.')
                sys.exit()

        create_html_template(html_template)
        sys.exit()

    elif (sys.argv[1] == "convert") or (sys.argv[1] == 'c'):
        in_file_name = None
        out_file_name = None
        tag = None
        counter = 1
        skip_convert = False

        for argument in sys.argv[2:]:
            counter += 1

            if skip_convert is True:
                skip_convert = False
                continue

            elif ("--file-in" in argument) or ("-i" in argument):
                skip_convert = True
                in_file_name = sys.argv[counter + 1].strip()

                if in_file_name.endswith('.html') is False:
                    print("WARNING: --file-in, -i.")
                    print("The file indicated doesn't have an \".html\" "
                          "suffix.")
                    sys.exit()

                if os.path.isfile(f"./{in_file_name}") is False:
                    print("WARNING: --file-in, -i.")
                    print("The input html file doesn't exist.")
                    sys.exit()

            elif ("--file-out" in argument) or ("-o" in argument):
                skip_convert = True
                out_file_name = sys.argv[counter + 1].strip()

                if out_file_name.endswith('.csv') is False:
                    print("WARNING: --file-out, -o.")
                    print('The output file doesn\'t have the ".csv" suffix.')
                    sys.exit()

                out_file_name_basic = out_file_name.replace(".csv",
                                                            "_basic.csv")
                out_file_name_cloze = out_file_name.replace(".csv",
                                                            "_cloze.csv")

                if os.path.isfile(f"./{out_file_name_basic}") is True:
                    print("WARNING: --file-out, -o.")
                    print(f'The file "{out_file_name_basic}" already exists'
                          ' in the current directory')
                    sys.exit()

                if os.path.isfile(f"./{out_file_name_cloze}") is True:
                    print("WARNING: --file-out, -o.")
                    print(f'The file "{out_file_name_cloze}" already exists'
                          ' in the current directory')
                    sys.exit()

            elif ("--tag" in argument) or ("-t" in argument):
                skip_convert = True
                tag = sys.argv[counter + 1].strip()

            else:
                print(f'"{argument}" is not a valid option for "convert".')
                sys.exit()

        # after checking all convert arguments:
        if in_file_name is None:
            print("WARNING: Input html file was not indicated.\nUse the \"-i\""
                  " option.")
            sys.exit()

        if out_file_name is None:
            out_file_name = in_file_name.replace(".html", ".csv")

            out_file_name_basic = out_file_name.replace(".csv",
                                                        "_basic.csv")
            out_file_name_cloze = out_file_name.replace(".csv",
                                                        "_cloze.csv")

            if os.path.isfile(f"./{out_file_name_basic}") is True:
                print("WARNING: --file-out, -o.")
                print(f'The file "{out_file_name_basic}" already exists'
                      ' in the current directory')
                sys.exit()

            if os.path.isfile(f"./{out_file_name_cloze}") is True:
                print("WARNING: --file-out, -o.")
                print(f'The file "{out_file_name_cloze}" already exists'
                      ' in the current directory')
                sys.exit()

        if tag is None:
            tag = in_file_name.replace(".html", "")

        list_of_flashcards = html_file_to_list(in_file_name)
        list_of_flashcards = strip_list_of_flashcards(list_of_flashcards, True)
        list_basics, list_clozes = list_to_basic_n_cloze(list_of_flashcards)

        if list_basics:
            write_basic_file(out_file_name_basic, list_basics, tag)

        if list_clozes:
            write_cloze_file(out_file_name_cloze, list_clozes, tag)

        sys.exit()

    else:
        print("Invalid Command. Enter \"html2anki -h\" for help.")
        sys.exit()


def create_html_template(html_template_path):
    """
    Create an html containing the template structure of the type of html file
    the program handles.
    """

    html_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>
    <style>
      body {
        text-align: center;
      }
      .flashcard, .flashcardcloze {
        border-style: solid;
        border-radius: 5px;
        margin-bottom: 20px;
        padding: 10px;
      }
      .frontback {
        size: 5px;
      }
      . cardnumber {
        background-color: blue;
      }
    </style>
  </head>
  <body>
    <h1 class="cardnumber">Card 1</h1>
    <div class="flashcard"> <!-- ****************************************** -->
      
      <hr class="frontback"/> <!-- ---------------------------------------- -->
      
    </div> <!-- *********************************************************** -->
  </body>
</html>
"""
    with open(f"./{html_template_path}", 'w') as file:
        file.write(html_template)
    print(f'The file "{html_template_path}" has been created.')


def html_file_to_list(file_path):
    """
    From a file path, returns every line of that file as a list of list of
    strings (one line, one string), where every list contain the lines of a
    flashcard
    """
    with open(file_path, 'r') as file_object:
        first_list = file_object.readlines()

    second_list = []
    temp_list = []  # contains the line of an individual flashcard.
    skip = False
    for line in first_list:
        if '<!DOCTYPE' in line:
            skip = True
        elif '<body>' in line:
            skip = False
            continue

        if skip is False:
            if 'class="cardnumber"' in line:
                pass
            elif ('class="flashcard"' in line) or \
                 ('class="flashcardcloze"' in line):
                # we append the current temporal list to second list.
                second_list.append(temp_list)
                # then delete the contents of temp_list.
                temp_list = []

                # and add the line that indicates the type of flashcard
                temp_list.append(line.rstrip('\n'))

            elif '</body>' in line:
                second_list.append(temp_list)
                del temp_list
                break
            else:
                temp_list.append(line.rstrip('\n'))
                # we begin again with the process of filling the temporal list.
        else:
            pass

    del second_list[0]  # this remove the first item (empty).

    return second_list


def strip_list_of_flashcards(list_of_flashcards, br_switch):
    """
    From a list of flashcards (one flashcard, one sub list) removes whitespace
    at the beginning and end of line (plus one whitespace at the end). If the
    content is inside a <pre> html tag, don't remove whitespace at all.
    The br_switch is True or False. If true, append a '<br>' to every line
    enclosed in <pre> and </pre> html tags, else, do nothing.
    """
    flashcards = []
    lines = []
    global br_line_in_pre_element

    for flashcard in list_of_flashcards:
        skip = False

        flashcards.append(lines)

        lines = []

        for line in flashcard:
            if '<pre' in line:
                lines.append(" " + line.strip())
                skip = True
                continue
            elif '</pre>' in line:
                skip = False

            if skip is False:
                lines.append(" " + line.strip())
            else:
                if br_switch is True:
                    lines.append(line + "<br>")
                if br_switch is False:
                    lines.append(line)

    flashcards.append(lines)

    del flashcards[0]

    return flashcards


def list_to_basic_n_cloze(list_of_flashcards):
    """
    From a list of flashcards create two list of flashcards:
    “list_flashcards_basic” and “list_flaschards_cloze”.
    """
    list_flashcards_basic = []
    list_flashcards_cloze = []

    for flashcard in list_of_flashcards:
        if 'class="flashcard">' in flashcard[0]:
            list_flashcards_basic.append(flashcard)

        elif 'class="flashcardcloze"' in flashcard[0]:
            list_flashcards_cloze.append(flashcard)

    return list_flashcards_basic, list_flashcards_cloze


def help_message():
    help_message = """HTML2ANKI HELP:
html2anki command [options]

Commands:

template:   Creates an html file containing the structure that the program can
            process.

            options:

            -f, --file  :   name of html file containing the template. If not
                            indicated, the file is named
                            "html2ankitemplate.html".

convert:    Converts an html file into a csv file ready to import to anki.

            options:

            -i, --file-in   :   Name of the file from which the user wants to
                                create the csv file. MANDATORY OPTION.

            -o, --file-out  :   Name of the csv that will be created by the
                                program. By defualt, the same file name of -i
                                (the ".html" suffix is changed by ".csv").
                                The suffix "_basic" and "_cloze" will be added
                                before the ".csv" automatically in order to
                                indicate the type of flashcards an html file
                                contains. Therefore, the program will check if
                                files with those same names exist.

            -t, --tag       :   Tag that is used by anki. By defualt, the name
                                of the input html file (-i) without the ".html"
                                suffix.
"""
    return help_message


def write_basic_file(file_path, list_of_flashcards, tag):
    with open(file_path, 'w') as f:
        f.write(';;\n')

    with open(file_path, 'a') as f:
        for flashcard in list_of_flashcards:
            f.write('"')
            for line in flashcard[1: len(flashcard) - 1]:
                # if 'class="flashcard"' in line:
                #     f.write('"')
                if 'class="frontback"' in line:
                    f.write('";"')
                # elif list_of_flashcards[len(list_of_flashcards) - 1] == line:
                #     f.write(f'";"{tag}"\n')
                else:
                    f.write(line.replace('"', '""'))
            if flashcard == list_of_flashcards[len(list_of_flashcards) - 1]:
                f.write(f'";"{tag}"')
            else:
                f.write(f'";"{tag}"\n')

    print('\n".csv" file with basic flashcards written:')
    print(file_path)


def write_cloze_file(file_path, list_of_flashcards, tag):
    with open(file_path, 'w') as f:
        f.write(';\n')

    with open(file_path, 'a') as f:
        for flashcard in list_of_flashcards:
            f.write('"')
            for line in flashcard[1: len(flashcard) - 1]:
                # if 'class="flashcardcloze"' in line:
                #     f.write('"')
                # elif list_of_flashcards[len(list_of_flashcards) - 1] == line:
                #     f.write(f'";"{tag}"\n')

                f.write(line.replace('"', '""'))
            if flashcard == list_of_flashcards[len(list_of_flashcards) - 1]:
                f.write(f'";"{tag}"')
            else:
                f.write(f'";"{tag}"\n')

    print('\n".csv" file with cloze flashcards written:')
    print(file_path)


if __name__ == "__main__":
    main()
