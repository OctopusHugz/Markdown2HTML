#!/usr/bin/python3
"""This module parses Markdown and converts it to HTML"""


def write_headers(line_content, header_level):
    header_tag = "<h" + str(header_level) + ">"
    closing_header_tag = "</h" + str(header_level) + ">"
    element_text = line_content[1:]
    element_text_string = " ".join(element_text)
    full_element_string = header_tag + element_text_string + \
        closing_header_tag + "\n"
    return full_element_string


def write_ul_list(my_list):
    list_string = "<ul>"
    list_closing_tag = "</ul>"
    for li in my_list:
        list_string += "<li>" + " ".join(li) + "</li>"
    full_list_string = list_string + list_closing_tag
    return full_list_string


def write_ol_list(my_list):
    list_string = "<ol>"
    list_closing_tag = "</ol>"
    for li in my_list:
        list_string += "<li>" + " ".join(li) + "</li>"
    full_list_string = list_string + list_closing_tag
    return full_list_string


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
    ul_items = {}
    ol_items = {}
    ul_li_list = []
    ol_li_list = []
    ul_flag = 0
    ol_flag = 0
    ul_elems = 0
    ol_elems = 0
    index = 0
    with open(argv[2], "w") as f:
        for line in file_content:
            line_content = line.split()
            header_level = line.count("#")
            # print("\nline is: {}".format(line))
            # print("line[0] is: {}".format(line[0]))
            # print("ul_flag is: {}".format(ul_flag))
            if header_level != 0:
                if ul_flag > 0:
                    f.write(write_ul_list(ul_items.get(ul_elems)))
                    f.write("\n")
                    ul_elems += 1
                    ul_li_list = []
                    ul_flag = 0
                elif ol_flag > 0:
                    f.write(write_ol_list(ol_items.get(ol_elems)))
                    f.write("\n")
                    ol_elems += 1
                    ol_li_list = []
                    ol_flag = 0
                f.write(write_headers(line_content, header_level))
            elif line[0] == "-" and ul_flag >= 0:
                ul_flag += 1
                ul_li_list.append(line_content[1:])
                ul_items.update({ul_elems: ul_li_list})
            elif line[0] != "-" and ul_flag > 0:
                print("Found the end of ul!")
                f.write(write_ul_list(ul_items.get(ul_elems)))
                f.write("\n")
                ul_elems += 1
                ul_li_list = []
                ul_flag = 0
                f.write(line)
            elif line[0] == "*" and ol_flag >= 0:
                ol_flag += 1
                ol_li_list.append(line_content[1:])
                ol_items.update({ol_elems: ol_li_list})
            elif line[0] != "*" and ol_flag > 0:
                print("Found the end of ol!")
                f.write(write_ol_list(ol_items.get(ol_elems)))
                f.write("\n")
                ul_elems += 1
                ul_li_list = []
                ol_flag = 0
                f.write(line)
            else:
                f.write(line)
            if index == len(file_content) - 1:
                if ul_flag > 0:
                    print("Found the end of ul!")
                    f.write(write_ul_list(ul_items.get(ul_elems)))
                    f.write("\n")
                elif ol_flag > 0:
                    print("Found the end of ol!")
                    f.write(write_ol_list(ol_items.get(ol_elems)))
                    f.write("\n")
            index += 1
