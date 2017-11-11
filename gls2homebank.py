#! /usr/bin/env python2

import argparse
import csv
from datetime import datetime

class gls(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL

csv.register_dialect("gls", gls)

glsFieldNames = ["kontonummer",
                  "buchungstag",
                  "wertstellung",
                  "beguenstigter",
                  "buchungstext",
                  "verwendungszweck1",
                  "verwendungszweck2",
                  "verwendungszweck3",
                  "verwendungszweck4",
                  "verwendungszweck5",
                  "verwendungszweck6",
                  "verwendungszweck7",
                  "verwendungszweck8",
                  "verwendungszweck9",
                  "verwendungszweck10",
                  "verwendungszweck11",
                  "verwendungszweck12",
                  "verwendungszweck13",
                  "verwendungszweck14",
                  "betrag",
                  "kontostand",
                  "waehrung"]

homebankFieldNames = ["date",
                      "paymode",
                      "info",
                      "payee",
                      "memo",
                      "amount",
                      "category",
                      "tags"]


def convertGlsGiro(filename):
    with open(filename, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(transactionLines(csvfile), dialect=dialect, fieldnames=glsFieldNames)

        with open("glsHomebank.csv", 'w') as outfile:
            writer = csv.DictWriter(outfile, dialect='gls', fieldnames=homebankFieldNames)
            for row in reader:
                writer.writerow(
                    {
                    'date': convertDate(row["buchungstag"]),
                    'paymode': 8,
                    'info': None,
                    'payee': row["beguenstigter"],
                    'memo':
                    row["verwendungszweck1"]+row["verwendungszweck2"]+row["verwendungszweck3"],
                    'amount': row["betrag"],
                    'category': None,
                    'tags': None
                    })

def transactionLines(file):
    lines = file.readlines()
    i = 1
    for line in lines:
        if "Betrag" in line:
            return lines[i:]
        i = i + 1

def convertDate(dateString):
    date = datetime.strptime(dateString, "%d.%m.%Y")
    return date.strftime('%d-%m-%Y')

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV export file from Germain GLS online banking to a Homebank compatible CSV format.")
    
    parser.add_argument("filename", help="The CSV file to convert.")

    args = parser.parse_args()

    convertGlsGiro(args.filename)
    print("GLS file converted. Output file: 'glsHomebank.csv'")


if __name__ == '__main__':
    main()
