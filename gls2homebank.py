#! /usr/bin/env python3

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

glsFieldNames = ["buchungstag",
                 "wertstellung",
                 "in-name",
                 "payee",
                 "kontonummer",
                 "IBAN",
                 "BLZ",
                 "BIC",
                 "verwendungszweck",
                 "kundenreferenz",
                 "waehrung",
                 "betrag", # TODO nun ohne minus und plus soll-haben stattdessen!
                 "soll-haben",]

homebankFieldNames = ["date",
                      "paymode",
                      "info",
                      "payee",
                      "memo",
                      "amount",
                      "category",
                      "tags"]


def convertGlsGiro(filename):
    with open(filename, 'r', encoding='iso-8859-1') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(transactionLines(csvfile), dialect=dialect, fieldnames=glsFieldNames)

        with open("glsHomebank.csv", 'w') as outfile:
            writer = csv.DictWriter(outfile, dialect='gls', fieldnames=homebankFieldNames)
            for row in reader:
                # "betrag" should be a negative value if "soll-haben" is "S"
                if row["soll-haben"] == "S":
                    row["betrag"] = "-"+row["betrag"]
                writer.writerow(
                    {
                    'date': convertDate(row["buchungstag"]),
                    'paymode': 8,
                    'info': None,
                    'payee': row["payee"],
                    'memo': row["verwendungszweck"].replace('\n', ' ').replace('\r', ''),
                    'amount': row["betrag"],
                    'category': None,
                    'tags': None
                    })

def transactionLines(file):
    lines = file.readlines()
    i = 1
    for line in lines:
        # Last line of header found
        if "Valuta" in line:
            return lines[i:-2] # delete last lines with "Anfangssaldo" etc. (I hope this is stable)
        i = i + 1

def convertDate(dateString):
    date = datetime.strptime(dateString, "%d.%m.%Y")
    return date.strftime('%m-%d-%Y')

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV export file from Germain GLS online banking to a Homebank compatible CSV format.")
    
    parser.add_argument("filename", help="The CSV file to convert.")

    args = parser.parse_args()

    convertGlsGiro(args.filename)
    print("GLS file converted. Output file: 'glsHomebank.csv'")


if __name__ == '__main__':
    main()
