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

            string = string[0:start] + string[end + 1:]

    return string
