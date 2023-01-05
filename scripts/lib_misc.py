import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def calc_exchange_rate(rates, value, currency):
    if currency == 'CAD':
        return value
    if currency not in rates:
        eprint("Error: Exchange rate for {} not found".format(currency))
        return value
    return value * rates[currency]
