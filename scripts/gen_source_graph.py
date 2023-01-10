from lib_config import *
from lib_graph import *
from lib_misc import *

import argparse
import os

import itertools
import numpy as np
import matplotlib.pyplot as plt

from enum import Enum
from os import path

GRAPH_TITLE = "{} Source Expenses".format(YEAR)
GRAPH_EXPORT_FILENAME = "gen_source_bar.png"

def sort_by_source(data):
    all_tags = set()
    all_tag_values = {}

    for monthly_txs in data["monthly_transactions"]:
        for tx in monthly_txs:
            source = tx.get_value("source")
            all_tags.add(source)
            if source not in all_tag_values:
                all_tag_values[source] = {CATEGORY_QUANTITY_KEY: 0, CATEGORY_PRICE_KEY: 0.0}

            all_tag_values[source][CATEGORY_QUANTITY_KEY] += 1
            all_tag_values[source][CATEGORY_PRICE_KEY] += tx.get_value("value")

    return (all_tags, all_tag_values)


def output_details(data):
    (_, all_tag_values) = sort_by_source(data)

    sorted_by_price = [(tag, (v[CATEGORY_PRICE_KEY], v[CATEGORY_QUANTITY_KEY])) for (tag, v) in all_tag_values.items()]
    sorted_by_price.sort(key=lambda x: x[CATEGORY_PRICE_KEY])
    for (k, v) in sorted_by_price:
        print(k.ljust(20), '\t{}'.format(v[CATEGORY_PRICE_KEY]), "\t{:.02f}".format(v[CATEGORY_QUANTITY_KEY]))

    monthly_transactions = [sum(tx.get_value("value") for tx in m) for m in data["monthly_transactions"]]

    print("Total:".ljust(20), '\t$\t{}'.format(sum(monthly_transactions)))


def gen_graph(data):
    (_, all_tag_values) = sort_by_source(data)

    sorted_by_price = [(tag, v[CATEGORY_PRICE_KEY]) for (tag, v) in all_tag_values.items()]
    sorted_by_price.sort(key=lambda x: x[1])

    prices = []
    xlabels = []
    for (tag, price) in sorted_by_price:
        if price > 0:
            continue
        prices.append(-price)
        xlabels.append(tag)

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_axes([0, 0, 1, 1])

    ax.set_title(GRAPH_TITLE, fontsize=FONT_SIZE)
    ax.tick_params(axis='both', which='major', labelsize=XTICK_SIZE)
    ax.set_xlabel("CAD $")
    ax.set_ylabel("Sources")
    ax.set_yticks(np.arange(len(xlabels)), fontsize=FONT_SIZE)
    ax.set_yticklabels(xlabels, fontsize=FONT_SIZE)

    xs = [i for i in range(0, len(xlabels))]

    ax.barh(xs, prices, color="#A89B8C")

    print("Exporting image to {}...".format(GRAPH_EXPORT_FILENAME))
    fig.savefig(GRAPH_EXPORT_FILENAME, bbox_inches='tight')
    print("Done!")


def run(args):
    files = args.files
    for file in files:
        toml_string = ""
        with open(file) as f:
            toml_string = f.read()
        data = get_data(toml_string)
        output_details(data)
        gen_graph(data)

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
