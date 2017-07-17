import csv
import xlrd

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
example_file = "example.csv"


def parse(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    print "\nList Comprehension"
    print "data[3][2]:"
    print data[3][2]

    print "\nCells in a nested loop:"
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if row == 50:
                print sheet.cell_value(row, col),

    print "\n\nROWS, COLUMNS, and CELLS:"
    print "Number of rows in the sheet:",
    print sheet.nrows
    print "Type of data in cell (row 3, col 2):",
    print sheet.cell_type(3, 2)
    print "Value in cell (row 3, col 2)",
    print sheet.cell_value(3, 2)
    print "Get a slice of values in column 3, from rows 1-3:"
    print sheet.col_values(3, start_rowx=1, end_rowx=4)

    print "\nDATES"
    print "Type of data in cell (row 1, col 0):",
    print sheet.cell_type(1, 0)
    exceltime = sheet.cell_value(1, 0)
    print "Time in Excel format:",
    print exceltime
    print "Convert time to a python datetime tuple, from the excel float:",
    print xlrd.xldate_as_tuple(exceltime, 0)


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    data = {
        'maxtime': (0, 0, 0, 0, 0, 0),
        'maxvalue': 0,
        'mintime': (0, 0, 0, 0, 0, 0),
        'minvalue': 0,
        'avgcoast': 0
    }

    maxvalue = float(sheet.cell_value(1, 1))
    minvalue = float(sheet.cell_value(1, 1))
    maxtime = float(sheet.cell_value(1, 0))
    mintime = float(sheet.cell_value(1, 0))
    total = 0.0

    for i in range(1, sheet.nrows):
        value = float(sheet.cell_value(i, 1))
        total += value
        if value > maxvalue:
            maxvalue = value
            maxtime = sheet.cell_value(i, 0)

        if value < minvalue:
            minvalue = value
            mintime = sheet.cell_value(i, 0)

    data['maxtime'] = xlrd.xldate_as_tuple(maxtime, 0)
    data['mintime'] = xlrd.xldate_as_tuple(mintime, 0)
    data['maxvalue'] = maxvalue
    data['minvalue'] = minvalue
    data['avgcoast'] = total / (sheet.nrows - 1)

    return data


# Lesson 2 Ques2
def xls_parse(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = [["Station", "Year", "Month", "Day", "Hour", "Max Load"]]

    for col in range(1, 9):
        data.append([sheet.cell_value(0, col).strip()])
        maxvalue = float(sheet.cell_value(1, col))
        maxtime = sheet.cell_value(1, 0)
        for row in range(1, sheet.nrows):
            value = float(sheet.cell_value(row, col))
            if value > maxvalue:
                maxvalue = float(sheet.cell_value(row, col))
                maxtime = sheet.cell_value(row, 0)
        time = xlrd.xldate_as_tuple(maxtime, 0)
        data[col].append(time[0])
        data[col].append(time[1])
        data[col].append(time[2])
        data[col].append(time[3])
        data[col].append(maxvalue)
    return data


def save_file(data, filename):
    with open(filename, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        for line in data:
            writer.writerow(line)
    csv_file.close()


def main():
    data = xls_parse(datafile)
    print data
    save_file(data, example_file)

main()
