from bs4 import BeautifulSoup

file_name = "airport.html"


def options(soup, id):
    option_values = []
    carrier_list = soup.find(id=id)
    for option in carrier_list.find_all("option"):
        option_values.append(option["value"])
    return option_values


def print_list(label, codes):
    print "\n%s:" % label
    for c in codes:
        print c


def extract_data(page):
    soup = BeautifulSoup(open(file_name), "lxml")
    data = {"eventvalidation": soup.find(id="__EVENTVALIDATION")["value"],
            "viewstate": soup.find(id="__VIEWSTATE")["value"]}
    return data


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        for options in soup.find(id="CarrierList").find_all("option"):
            if "All" not in options["value"]:
                data.append(options["value"])

    return data


def checkInt(st):
    try:
        int(st)
        return True
    except ValueError:
        return False


# def process_file(f):
#     """
#     This function extracts data from the file given as the function argument in
#     a list of dictionaries. This is example of the data structure you should
#     return:
#
#     data = [{"courier": "FL",
#              "airport": "ATL",
#              "year": 2012,
#              "month": 12,
#              "flights": {"domestic": 100,
#                          "international": 100}
#             },
#             {"courier": "..."}
#     ]
#
#
#     Note - year, month, and the flight data should be integers.
#     You should skip the rows that contain the TOTAL data for a year.
#     """
#     data = []
#     info = {}
#     info["courier"], info["airport"] = f[:6].split("-")
#     # Note: create a new dictionary for each entry in the output data list.
#     # If you use the info dictionary defined here each element in the list
#     # will be a reference to the same info dictionary.
#     with open("{}/{}".format(datadir, f), "r") as html:
#
#         soup = BeautifulSoup(html, "lxml")
#         table = soup.find(id="DataGrid1")
#         for tr in table.find_all("tr"):
#             row = {"courier": info["courier"], "airport": info["airport"]}
#             temp = []
#             for td in tr.find_all("td"):
#                 temp.append(td.getText())
#             if checkInt(temp[1]) == False:
#                 continue
#             row["year"] = int(temp[0])
#             row["month"] = int(temp[1])
#             row["flights"] = {}
#             if temp[2] != "":
#                 row["flights"]["domestic"] = int(temp[2].replace(',',''))
#             else:
#                 row["flights"]["domestic"] = 0
#             if temp[3] != "":
#                 row["flights"]["international"] = int(temp[3].replace(',',''))
#             else:
#                 row["flights"]["international"] = 0
#             data.append(row)
#         print data
#
#     return data


def main():
    soup = BeautifulSoup(open(file_name), "lxml")

    codes = options(soup, "CarrierList")
    print_list("Carriers", codes)

    codes = options(soup, "AirportList")
    print_list("Airports", codes)

main()
