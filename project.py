import xml.etree.cElementTree as ET
import pprint
import re

OSM_FILE = "chicago_illinois.osm"
OSM_FILE_PART = "chicago_part.osm"
STREETS_FILE = "streets.txt"

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_names = []

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Broadway"]

mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Ave.": "Avenue",
           "Rd": "Road",
           "Rd.": "Road"
           }


def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")


def update_street_name(name, group, mapping=mapping):
    # name = name.replace(".", "")
    for key, value in mapping.iteritems():
        if value in name:
            break
        elif key in group:
            # print "Before:", name
            name = name.replace(key, mapping[key])
            # print "After:", name
            # if name[-1] == ".":
            #     name = name.replace(".", "")
            break
    street_names.append(name)


def audit_street_name(street_name):
    m = street_type_re.search(street_name)
    if m:
        if m.group() not in expected:
            # print m.group()
            update_street_name(street_name, m.group())
            return
    street_names.append(street_name)


def audit_file(file_name):
    osm_file = open(file_name, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if is_street_name(elem):
            audit_street_name(elem.attrib["v"])
    osm_file.close()
    # pprint.pprint(list(street_names))
    # print street_names
    with open(STREETS_FILE, "w") as st_file:
        for st in sorted(street_names):
            st_file.write(st+"\n")


audit_file(OSM_FILE_PART)
