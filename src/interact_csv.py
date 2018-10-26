import csv

def getSearchDict():
    to_search = {}

    with open('enter_data_to_be_searched.csv') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # Rewind.
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        if has_header:
            next(reader)  # Skip header row.
        for row in reader:
            destination = row[1]
            itemId = row[0]
            if not to_search.get(destination):
                to_search[destination] = []
            to_search[destination].append(itemId)
    return to_search
