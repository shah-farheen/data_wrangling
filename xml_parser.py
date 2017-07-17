import xml.etree.ElementTree as ET

article_file = "exampleresearcharticle.xml"


def get_root(file_name):
    tree = ET.parse(file_name)
    return tree.getroot()


def print_line(line_num, file):
    with open(file, "r") as f:
        for i, line in enumerate(f):
            if i == line_num:
                print line


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.

    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    split_line = '<?xml version="1.0" encoding="UTF-8"?>'
    whole_file = open(filename, "r")
    count = 0
    global new_file
    # new_file.close()
    for i, line in enumerate(whole_file):
        if line.strip() == split_line:
            new_file = open("{}-{}".format(filename, count), "wb")
            count += 1
        new_file.write(line)

    pass


def get_authors(root):
    authors = []
    for author in root.findall('./fm/bibl/aug/au'):
        data = {
            "fnm": author.find("fnm").text,
            "snm": author.find("snm").text,
            "email": author.find("email").text,
            "insr": []
        }
        for insr in author.findall('./insr'):
            data["insr"].append(insr.attrib['iid'])
        authors.append(data)

    return authors


def main():
    root = get_root(article_file)
    data = get_authors(root)
    print data


main()
