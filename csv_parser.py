import csv


def parse(datafile):
    data = []
    keys = []
    count = 1
    with open(datafile, "rb") as f:
        for line in f:
            # if(count == 12):
            # 	f.close()
            # 	return data
            if count == 1:
                keys = line.strip().split(',')
            else:
                dictionary = {}
                row = line.strip().split(',')
                for i in range(0, len(keys)):
                    dictionary[keys[i]] = row[i]
                data.append(dictionary)
            count += 1
        return data


def parse_csv(datafile):
    data = []
    with open(datafile, "rb") as f:
        r = csv.DictReader(f)  # r is an instance(object) of DictReader
        # print r,"\n\n"
        for line in r:
            data.append(line)
        return data


# Lesson 2 Quiz 1
def parse_file(datafile):
    name = ""
    data = []
    with open(datafile, 'rb') as f:
        r = csv.reader(f)
        firstline = r.next()
        name = firstline[1]
        # print name
        r.next()
        for row in r:
            data.append(row)
        # print data
        pass
    # Do not change the line below
    return name, data


def start():
    data = parse_csv("beatles-discography.csv")
    for d in data:
        print d


start()
