#!/usr/bin/python3

import argparse
import os
from os import path

import toml

from lib_graph import *

def csv_to_toml(toml_string):
    parsed_toml = toml.loads(toml_string)
    items = parsed_toml["item"]

    columns = list(items[0].keys())
    print(",".join(columns))

    for item in items:
        tx = Transaction(item)
        print(tx.to_csv_row(columns))


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
