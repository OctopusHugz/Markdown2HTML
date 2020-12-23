#!/usr/bin/python3
"""This module parses Markdown and converts it to HTML"""
if __name__ == "__main__":
    from sys import argv, exit, stderr
    from os import path

    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)
    if not (path.exists(argv[1])):
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)
    with open(argv[1]) as f:
        file_content = f.readlines()
    index = 0
    line_array = []
    for line in file_content:
        header_level = line.count("#")
        header_tag = "<h" + str(header_level) + ">"
        closing_header_tag = "</h" + str(header_level) + ">"
        line_content = line.split()
        line_content[index] = header_tag
        element_text = line_content[1:]
        element_text_string = " ".join(element_text)
        full_element_string = header_tag + element_text_string + closing_header_tag + "\n"
        line_array.append(full_element_string)
    with open(argv[2], "w+") as f:
        for line in line_array:
            f.write(line)
