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
