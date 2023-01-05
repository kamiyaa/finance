#!/usr/bin/python3

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

GRAPH_TITLE = "{} Monthly Profit".format(YEAR)
GRAPH_EXPORT_FILENAME = "gen_monthly_profit.png"

def get_monthly_sums(data):
    exchange_rates = data['exchange_rate']
    monthly_transactions = data["monthly_transactions"]

    monthly_totals = []
    for month in monthly_transactions:
        monthly_total = 0
        for tx in month:
            tx_currency = tx.get_value("currency")
            monthly_total += calc_exchange_rate(
                exchange_rates,
                tx.get_value("value"),
                tx_currency)
        monthly_totals.append(monthly_total)
    return monthly_totals

def gen_graph(files):
    all_monthly_transactions = [0 for i in range(12)]

    for file in files:
        toml_string = ""
        with open(file) as f:
            toml_string = f.read()
        data = get_data(toml_string)

        monthly_transactions = get_monthly_sums(data)
        for (i, m) in enumerate(monthly_transactions):
            all_monthly_transactions[i] += m

    monthly_aggregate_transactions = np.cumsum(all_monthly_transactions)

    # Graphing

    print("Month\tTransactions")
    for i, m in enumerate(monthly_transactions):
        print("{:02d}\t$ {:.02f}".format(i + 1, m))
    print("Total:\t$ {:.02f}".format(sum(monthly_transactions)))

    font = {'family' : FONT_FAMILY,
            'weight' : 'bold',
            'size'   : FONT_SIZE}
    plt.rc('font', **font)

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_axes([0, 0, 1, 1])

    months = np.arange(1, 13)

    ax.set_title(GRAPH_TITLE)
    ax.set_ylabel("CAD $", fontsize=FONT_SIZE)
    ax.set_xlabel("Month", fontsize=FONT_SIZE)
    ax.set_xticks(months)

    ax.fill_between(months, 0, monthly_aggregate_transactions, color="#A89B8C")
    ax.fill_between(months, 0, monthly_transactions, color="#F0DFAD")

    for (i, v) in enumerate(monthly_aggregate_transactions):
        ax.text(i + 0.7, v + 2,
                "{:.02f}".format(v),
                color='#1E2749',
                fontweight='normal',
                fontsize=FONT_SIZE)

    for (i, v) in enumerate(monthly_transactions):
        ax.text(i + 0.7, v + 2,
                "{:.02f}".format(v),
                color='#1E2749',
                fontweight='normal',
                fontsize=FONT_SIZE)

    print("Exporting image to {}...".format(GRAPH_EXPORT_FILENAME))
    fig.savefig(GRAPH_EXPORT_FILENAME, bbox_inches='tight')
    print("Done!")

def run(args):
    files = args.files
    gen_graph(files)

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
