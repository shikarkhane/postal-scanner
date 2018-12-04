import csv
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')


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


def utf_encode(x):
    return x.encode('utf-8')


def writeDictToCSV(data):
    with open('result.csv', 'w') as csvfile:
        fieldnames = ['destination', 'itemId', 'delivered', 'time', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for destination in data:
            for row in data[destination]:
                try:
                    writer.writerow({'destination': utf_encode(destination), 'itemId': utf_encode(row[0]),
                                     'delivered': row[1], 'time': utf_encode(row[2]),
                                     'status': utf_encode(row[3])})
                except Exception as e:
                    logging.exception(e)
                    logging.exception(str(row))
