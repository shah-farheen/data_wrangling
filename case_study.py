from collections import defaultdict
import xml.etree.cElementTree as ET
import pprint
import re

OSM_FILE = "chicago_illinois.osm"
OSM_FILE_PART = "chicago_part.osm"


#3
def count_tags(filename):
    # YOUR CODE HERE
    tag_counts = defaultdict(int)
    for event, elem in ET.iterparse(filename):
        tag_counts[elem.tag] += 1
    return tag_counts


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


#7
def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        k = element.attrib["k"]
        if lower.search(k):
            keys["lower"] += 1
        elif lower_colon.search(k):
            keys["lower_colon"] += 1
        elif problemchars.search(k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
        pass

    return keys


#8
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        tag = element.tag
        if (tag == "node") or (tag == "way") or (tag == "relation"):
            users.add(element.attrib["uid"])
        pass

    return users


#11
def update_name(name, mapping):
    # YOUR CODE HERE
    for key in mapping:
        if key in name:
            name = name.replace(key, mapping[key])
            if "." in name:
                name = name.replace(".", "")
            break
    return name


#12
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["id"] = element.attrib["id"]
        node["type"] = element.tag
        if "visible" in element.attrib:
            node["visible"] = element.attrib["visible"]
        node["created"] = {"version": element.attrib["version"],
        "changeset": element.attrib["changeset"], "timestamp": element.attrib["timestamp"],
        "user": element.attrib["user"], "uid": element.attrib["uid"]}
        node["address"] = {}

        if element.tag == "way":
            node["node_refs"] = []
        else:
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]

        for tag in element.iter("tag"):
            if problemchars.search(tag.attrib["k"]):
                continue
            elif "addr:" in tag.attrib["k"]:
                addr = tag.attrib["k"].split(":")
                if len(addr) > 2:
                    continue
                node["address"][addr[1]] = tag.attrib["v"]
            else:
                node[tag.attrib["k"]] = tag.attrib["v"]

        for nd in element.iter("nd"):
            node["node_refs"].append(nd.attrib["ref"])

        if not bool(node["address"]):
            node.pop("address", None)

        return node
    else:
        return None


def main():
    tag_counts = count_tags(OSM_FILE_PART)
    pprint.pprint(tag_counts)


main()
