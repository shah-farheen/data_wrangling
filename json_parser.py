import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

WEATHER_BASE_URL = "http://samples.openweathermap.org/data/2.5/weather"
WEATHER_APP_ID = "b1b15e88fa797225412429c1c50c122a1"

query_type = {"simple": {},
               "atr": {"inc": "aliases+tags+ratings"},
               "aliases": {"inc": "aliases"},
               "releases": {"inc": "releases"}}


def query_weather(url, place):
    params = {"appid": WEATHER_APP_ID, "q": place}
    r = requests.get(url, params=params)
    print "requesting:", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


# main function to make queries which return a json document
def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting:", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


# query by artist's name
def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    # results = query_weather(WEATHER_BASE_URL, "delhi,IN")
    pretty_print(results)
    print "\n\nFORMATION DATE:"
    print results["artists"][0]["life-span"]["begin"]

    # Ques 4; Ans = 90s US grunge band
    # for ar in results["artists"]:
    #     if "tags" in ar:
    #         for tag in ar["tags"]:
    #             if "kurt" in tag["name"]:
    #                 print "\n\nDISAMBIGUATION:"
    #                 print ar["disambiguation"]
    #                 break

    # Ques 3; Ans = Los Beatles
    # for ar in results["artists"]:
    #     if ar["name"] == "The Beatles":
    #         for al in ar["aliases"]:
    #             if al["locale"] == "es":
    #                 print "\n\nALIAS NAME"
    #                 print al["name"]
    #                 break
    #         break

    # Ques 2; Ans = London
    # for ar in results["artists"]:
    #     if "group" in ar["disambiguation"]:
    #         print "\n\nBEGIN-AREA NAME"
    #         print ar["begin-area"]["name"]
    #         break

    # Ques 1; Ans = 2
    # count = 0
    # for ar in results["artists"]:
    #     if ar["name"] == "First Aid Kit":
    #         count += 1
    #
    # print "\n\nNUMBER:"
    # print count

    # print "\nARTIST:"
    # pretty_print(results["artists"][3])
    #
    # artist_id = results["artists"][3]["id"]
    # artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    # releases = artist_data["releases"]
    #
    # print "\nOne Release:"
    # pretty_print(releases[0], 2)
    #
    # release_titles = [r["title"] for r in releases]
    # print "\nALL TITLES:"
    # for t in release_titles:
    #     print t


main()
