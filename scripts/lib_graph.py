from dataclasses import dataclass, asdict

import datetime

import toml

KEY_EXCHANGE_RATE = 'KEY_EXCHANGE_RATE'
KEY_TRANSACTIONS = 'transactions'
KEY_TRANSACTIONS_BY_MONTH = 'transactions_by_month'

## classes

@dataclass
class Transaction:
    date: datetime.datetime
    description: str
    source: str
    value: float
    currency: str
    category: str
    tags: list[str]

    def __init__(self, dict_data = {}):
        self.date = dict_data.get('date', None)
        self.description = dict_data.get('description', '')
        self.source = dict_data.get('source', '')
        self.value = dict_data.get('value', 0.0)
        self.currency = dict_data.get('currency', 'CAD')
        self.category = dict_data.get('category', '')
        self.tags = dict_data.get('tags', [])

    def to_csv_row(self, columns):
        values = []
        self_dict = asdict(self)
        for column in columns:
            if column in self_dict:
                value = self_dict.get(column)
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

    def as_dict(self):
        return asdict(self)

@dataclass
class TransactionList:
    transactions: list[Transaction]
    transactions_by_month: list[list[Transaction]]
    exchange_rates: dict[str, float]

    def __init__(self,
        transactions: list[Transaction] = [],
        transactions_by_month: list[list[Transaction]] = [[] for i in range(12)],
        exchange_rates: dict[str, float] = {
            "USD": 1.35
        }):
        self.transactions = transactions
        self.transactions_by_month = transactions_by_month
        self.exchange_rates = exchange_rates

    def populate(self, toml_data):
        exchange_rates = toml_data.get(KEY_EXCHANGE_RATE, {})
        for (k, v) in exchange_rates.items():
            self.exchange_rates[k] = v

        items = toml_data.get(KEY_TRANSACTIONS, [])

        for item in items:
            tx = Transaction(item)
            item_index = tx.date.month - 1
            self.transactions.append(tx)
            self.transactions_by_month[item_index].append(tx)

    def sort_by_date(self):
        self.transactions.sort(key=lambda tx : tx.date)
        for i in range(len(self.transactions_by_month)):
            self.transactions_by_month[i].sort(key=lambda tx : tx.date)

## functions

def populate_data(data: TransactionList, toml_string):
    toml_data = toml.loads(toml_string)
    exchange_rates = toml_data.get(KEY_EXCHANGE_RATE, {})
    for (k, v) in exchange_rates.items():
        data[KEY_EXCHANGE_RATE][k] = v

    items = toml_data.get(KEY_TRANSACTIONS, [])

    for item in items:
        tx = Transaction(item)
        item_index = tx.date.month - 1
        data[KEY_TRANSACTIONS_BY_MONTH][item_index].append(tx)

    return data
