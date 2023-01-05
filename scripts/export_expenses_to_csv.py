#!/usr/bin/python3

import argparse
import os
from os import path

import toml

from lib_graph import *

COLUMNS = [
    "date",
    "paid to",
    "description",
    "total amount paid (inc. hst/gst)",
    "currency",
    "tags",
]

COLUMNS_MAP = {
    "date": "date",
    "paid to": "source",
    "description": "description",
    "total amount paid (inc. hst/gst)": "value",
    "currency": "currency",
    "tags": "tags",
}

COLUMN_IDS = [ COLUMNS_MAP[col] for col in COLUMNS ]

def toml_to_csv(toml_string):
    parsed_toml = toml.loads(toml_string)
    items = parsed_toml["item"]

    print(",".join(COLUMNS))

    for item in items:
        tx = Transaction(item)
        print(tx.to_csv_row(COLUMN_IDS))


def run(args):
    files = args.files
    for file in files:
        toml_string = ""
        with open(file) as f:
            toml_string = f.read()

        toml_to_csv(toml_string)


def main():
    parser = argparse.ArgumentParser(
        prog = 'toml_to_csv',
        description = 'convert toml to csv',
        epilog = 'Text at the bottom of help')
    parser.add_argument('files', nargs='+',
                        help='files')

    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
