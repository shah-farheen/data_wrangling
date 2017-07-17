import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import csv
import types

OSM_FILE = "chicago_illinois.osm"
OSM_FILE_PART = "chicago_part.osm"

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_type(value):
    if value == "NULL" or "":
        return types.NoneType
    elif value[0] == "{":
        return list
    elif is_int(value):
        return int
    elif is_float(value):
        return float
    else:
        return str


def audit_file(filename, fields):
    fieldtypes = {}
    for field in fields:
        fieldtypes[field] = set()
    file = open(filename, "r")
    reader = csv.DictReader(file)
    for row in reader:
        if "dbpedia.org" in row["URI"]:
            for field in fields:
                fieldtypes[field].add(get_type(row[field]))

    # YOUR CODE HERE
    return fieldtypes


def fix_area(area):
    # YOUR CODE HERE
    if area == "NULL" or "":
        return None
    elif is_float(area):
        return float(area)
    else:
        area = area.replace("{", "")
        area = area.replace("}", "")
        areas = area.split("|")
        if len(areas[0]) >= len(areas[1]):
            return float(areas[0])
        else:
            return float(areas[1])


def fix_name(name):
    # YOUR CODE HERE
    if name[0] == "{":
        name = name.replace("{", "")
        name = name.replace("}", "")
        return name.split("|")
    elif name == "NULL" or "":
        return []
    else:
        return [name]


def check_loc(point, lat, longi):
    # YOUR CODE HERE
    points = point.split()
    if (points[0] == lat) and (points[1] == longi):
        return True
    else:
        return False
    pass


def process_file(input_file, output_good, output_bad):
    global year
    global int_year
    out_good = []
    out_bad = []

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        #COMPLETE THIS FUNCTION
        for line in reader:
            if "dbpedia.org" in line["URI"]:
                if line["productionStartYear"] != "NULL":
                    year = line["productionStartYear"][:4]
                    int_year = int(year)
                    line["productionStartYear"] = year
                    if int_year >= 1886 and int_year <= 2014:
                        out_good.append(line)
                    else:
                        out_bad.append(line)
                else:
                    out_bad.append(line)



    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    with open(output_good, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in out_good:
            writer.writerow(row)

    with open(output_bad, "w") as b:
        writer = csv.DictWriter(b, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in out_bad:
            writer.writerow(row)


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1


def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)


def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib["k"] == "addr:street")


def audit():
    for event, elem in ET.iterparse(OSM_FILE_PART):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib["v"])
    print_sorted_dict(street_types)

# audit()


def test():
    print float("1.13959e+07")
    print float("1.14e+07")

test()
