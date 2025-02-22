import pathlib
import re


def path_exists(path: str) -> bool:
    """
    Checks if file or directory in str exists. Returns True if exist, False
    otherwise.
    """
    file_path = pathlib.Path(path)
    return file_path.exists()


def out_files_exists(
    prefix_path: str | None, input_file: pathlib.Path
) -> tuple[bool, str]:
    """
    Checks whether output file to be created already exists. If true,
    returns tuple(True, <error message>).
    """
    error: bool = False
    existing_files: list[str] = []
    prefix: str
    if not prefix_path:
        prefix = re.sub(r"\..*$", "", input_file.name)
    else:
        prefix = prefix_path

    if path_exists(prefix + "_basic.tsv"):
        existing_files.append(prefix + "_basic.tsv")
        error = True
    if path_exists(prefix + "_cloze.tsv"):
        existing_files.append(prefix + "_cloze.tsv")
        error = True

    error_message = "Error: the following output files already exists:\n"
    for s in existing_files:
        error_message += f"{s}\n"

    return (error, error_message)


def clean_html_comments(string):
    """
    Input: string that contains html source code.
    Output: string that contains html source code without html comments.
    """
    while True:
        if string.find("<!--") == -1:
            return string
        else:
            start = string.find("<!--")
            end = string.find("-->") + 2

            string = string[0:start] + string[end + 1 :]

    return string
