def strip_str(st):
    if st == "NULL":
        return None
    else:
        return st.strip()


def add_to_dict(_dict, key, value):
    _dict[key] = value


def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            # YOUR CODE HERE
            if line["rdf-schema#label"][-1] == ")":
                line["rdf-schema#label"] = line["rdf-schema#label"][:line["rdf-schema#label"].index('(')-1].strip()

            if (line["name"] == "NULL") or (not line["name"].isalnum()):
                line["name"] = line["rdf-schema#label"]
            else:
                line["name"] = line["name"].strip()

            line["URI"] = strip_str(line["URI"])
            line["synonym"] = strip_str(line["synonym"])
            line["rdf-schema#comment"] = strip_str(line["rdf-schema#comment"])
            line["family_label"] = strip_str(line["family_label"])
            line["class_label"] = strip_str(line["class_label"])
            line["phylum_label"] = strip_str(line["phylum_label"])
            line["order_label"] = strip_str(line["order_label"])
            line["kingdom_label"] = strip_str(line["kingdom_label"])
            line["genus_label"] = strip_str(line["genus_label"])

            if line["synonym"] != None:
                line["synonym"] = parse_array(line["synonym"])

            temp_dict = {}
            add_to_dict(temp_dict, fields["rdf-schema#label"], line["rdf-schema#label"])
            add_to_dict(temp_dict, fields["rdf-schema#comment"], line["rdf-schema#comment"])
            add_to_dict(temp_dict, fields["URI"], line["URI"])
            add_to_dict(temp_dict, fields["synonym"], line["synonym"])
            add_to_dict(temp_dict, fields["name"], line["name"])

            class_dict = {}
            add_to_dict(class_dict, fields["family_label"], line["family_label"])
            add_to_dict(class_dict, fields["class_label"], line["class_label"])
            add_to_dict(class_dict, fields["kingdom_label"], line["kingdom_label"])
            add_to_dict(class_dict, fields["phylum_label"], line["phylum_label"])
            add_to_dict(class_dict, fields["order_label"], line["order_label"])
            add_to_dict(class_dict, fields["genus_label"], line["genus_label"])
            temp_dict["classification"] = class_dict

            data.append(temp_dict)
            pass
    return data
