#!/usr/bin/python3
"""This module parses Markdown and converts it to HTML"""


def write_headers(line_content, header_level):
    header_tag = "<h" + str(header_level) + ">"
    closing_header_tag = "</h" + str(header_level) + ">"
    element_text = line_content[1:]
    element_text_string = " ".join(element_text)
    element_text_string = element_text_string.replace("**", "<b>", 1)
    element_text_string = element_text_string.replace("**", "</b>", 1)
    element_text_string = element_text_string.replace("__", "<em>", 1)
    element_text_string = element_text_string.replace("__", "</em>", 1)
    full_element_string = header_tag + element_text_string + \
        closing_header_tag + "\n"
    return full_element_string


def write_ul_list(my_list):
    list_string = "<ul>"
    list_closing_tag = "</ul>"
    for li in my_list:
        for li_string in li:
            if "[[" in li_string and "]]" in li_string:
                starting_index = li_string.index("[[")
                ending_index = li_string.index("]]")
                md5_string = li_string[starting_index + 2:ending_index]
                strings = li_string.split(md5_string)
                strings[0] = strings[0].replace("[[", "")
                strings[1] = strings[1].replace("]]", "")
                hash_obj = md5(md5_string.encode())
                hashed_string = hash_obj.hexdigest()
                li_string = strings[0] + hashed_string + strings[1]
                li = list(li_string)
        if len(li) != 32:
            list_string += "<li>" + " ".join(li) + "</li>"
        else:
            list_string += "<li>" + "".join(li) + "</li>"
    full_list_string = list_string + list_closing_tag
    if full_list_string.count("**") == 2:
        full_list_string = full_list_string.replace("**", "<b>", 1)
        full_list_string = full_list_string.replace("**", "</b>", 1)
    if full_list_string.count("__") == 2:
        full_list_string = full_list_string.replace("__", "<em>", 1)
        full_list_string = full_list_string.replace("__", "</em>", 1)
    return full_list_string


def write_ol_list(my_list):
    list_string = "<ol>"
    list_closing_tag = "</ol>"
    for li in my_list:
        for li_string in li:
            if "[[" in li_string and "]]" in li_string:
                starting_index = li_string.index("[[")
                ending_index = li_string.index("]]")
                md5_string = li_string[starting_index + 2:ending_index]
                strings = li_string.split(md5_string)
                strings[0] = strings[0].replace("[[", "")
                strings[1] = strings[1].replace("]]", "")
                hash_obj = md5(md5_string.encode())
                hashed_string = hash_obj.hexdigest()
                li_string = strings[0] + hashed_string + strings[1]
                li = list(li_string)
        if len(li) != 32:
            list_string += "<li>" + " ".join(li) + "</li>"
        else:
            list_string += "<li>" + "".join(li) + "</li>"
    full_list_string = list_string + list_closing_tag
    if full_list_string.count("**") == 2:
        full_list_string = full_list_string.replace("**", "<b>", 1)
        full_list_string = full_list_string.replace("**", "</b>", 1)
    if full_list_string.count("__") == 2:
        full_list_string = full_list_string.replace("__", "<em>", 1)
        full_list_string = full_list_string.replace("__", "</em>", 1)
    return full_list_string


def write_p_lines(p_lines):
    list_string = "<p>\n"
    list_closing_tag = "</p>\n"
    index = 0
    for line in p_lines:
        if len(p_lines) == 1:
            list_string += line
        else:
            if index != len(p_lines) - 1:
                list_string += line + "<br />\n"
            else:
                list_string += line
        index += 1
    full_list_string = list_string + list_closing_tag
    return full_list_string


if __name__ == "__main__":
    from sys import argv, exit, stderr
    from os import path
    from hashlib import md5

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
    p_lines = []
    with open(argv[2], "w") as f:
        for line in file_content:
            line_content = line.split()
            header_level = line.count("#")
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
                f.write(write_ul_list(ul_items.get(ul_elems)))
                f.write("\n")
                ul_elems += 1
                ul_li_list = []
                ul_flag = 0
                f.write(line)
            elif line[0] == "*" and line[1] != "*" and ol_flag >= 0:
                ol_flag += 1
                ol_li_list.append(line_content[1:])
                ol_items.update({ol_elems: ol_li_list})
            elif line[0] != "*" and ol_flag > 0:
                f.write(write_ol_list(ol_items.get(ol_elems)))
                f.write("\n")
                ol_elems += 1
                ol_li_list = []
                ol_flag = 0
                f.write(line)
            elif "((" in line and "))" in line:
                starting_index = line.index("((")
                ending_index = line.index("))")
                strip_c_string = line[starting_index + 2:ending_index]
                strings = line.split(strip_c_string)
                strings[0] = strings[0].replace("((", "")
                strings[1] = strings[1].replace("))", "")
                strip_c_string = strip_c_string.replace("c", "")
                strip_c_string = strip_c_string.replace("C", "")
                strip_c_string = strip_c_string.replace("((", "")
                strip_c_string = strip_c_string.replace("))", "")
                c_less_string = strings[0] + strip_c_string + strings[1]
                c_less_string = c_less_string.replace("**", "<b>", 1)
                c_less_string = c_less_string.replace("**", "</b>", 1)
                c_less_string = c_less_string.replace("__", "<em>", 1)
                c_less_string = c_less_string.replace("__", "</em>", 1)
                p_lines.append(c_less_string)
            elif "[[" in line and "]]" in line:
                starting_index = line.index("[[")
                ending_index = line.index("]]")
                md5_string = line[starting_index + 2:ending_index]
                strings = line.split(md5_string)
                strings[0] = strings[0].replace("[[", "")
                strings[1] = strings[1].replace("]]", "")
                hash_obj = md5(md5_string.encode())
                hashed_string = hash_obj.hexdigest()
                full_hashed_string = strings[0] + hashed_string + strings[1]
                p_lines.append(full_hashed_string)
            else:
                if line != "\n":
                    if line.count("**") == 2:
                        line = line.replace("**", "<b>", 1)
                        line = line.replace("**", "</b>", 1)
                    if line.count("__") == 2:
                        line = line.replace("__", "<em>", 1)
                        line = line.replace("__", "</em>", 1)
                    p_lines.append(line)
                else:
                    if len(p_lines) > 0:
                        f.write(write_p_lines(p_lines))
                        p_lines = []
            if index == len(file_content) - 1:
                if ul_flag > 0:
                    f.write(write_ul_list(ul_items.get(ul_elems)))
                    f.write("\n")
                elif ol_flag > 0:
                    f.write(write_ol_list(ol_items.get(ol_elems)))
                    f.write("\n")
                elif len(p_lines) > 0:
                    f.write(write_p_lines(p_lines))
            index += 1
