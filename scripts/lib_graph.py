import toml

import datetime

## classes

class Transaction:
    def __init__(self, dict_data = {}):
        self._dict = dict_data

    def set_value(self, key, value):
        self._dict[key] = value

    def get_value(self, key):
        return self._dict[key]

    # transformations
    def from_dict(dict_data):
        tx = Transaction(dict_data)
        return tx

    def to_csv_row(self, columns):
        values = []
        for column in columns:
            if column in self._dict:
                value = self.get_value(column)
                if isinstance(value, list):
                    values.append(value[0])
                # elif isinstance(value, datetime.datetime):
                #     values.append("{}-{:02}-{:02}".format(value.year, value.month, value.day))
                elif isinstance(value, str):
                    values.append(str(value.replace(",", " ")))
                # elif isinstance(value, int)):
                #     values.append(str(value))
                else:
                    values.append(str(value))    

        return ",".join(values)

## functions

def get_data(toml_string):
    monthly_transactions = [[] for i in range(12)]
    data = toml.loads(toml_string)
    
    exchange_rate = data['exchange_rate']
    
    items = data['item']
    for item in items:
        tx = Transaction.from_dict(item)
        monthly_transactions[tx.get_value("date").month - 1].append(tx)

    return {
        "exchange_rate": exchange_rate,
        "balance_sheet": items,
        "monthly_transactions": monthly_transactions
    }
