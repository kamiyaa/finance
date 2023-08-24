#!/usr/bin/python3

import argparse
import os
from os import path

import toml

from lib_graph import *
from lib_misc import *

def csv_to_toml(data: TransactionList):
    items = data.transactions
    if len(items) == 0:
        return

    columns = list(items[0].as_dict().keys())
    print(",".join(columns))

    for item in items:
        tx = Transaction(item)
        print(tx.to_csv_row(columns))



def run(args):
    files = args.files
    data = TransactionList()
    for file in files:
        parsed_toml = toml.load(file)
        data.populate(parsed_toml)

    data.sort_by_date()
    csv_to_toml(data)

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
