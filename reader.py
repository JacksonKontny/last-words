from csv import DictReader
import csv
import os
import random


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(DIR_PATH, 'data')
LAST_WORDS_PATH = os.path.join(DATA_PATH, 'lastwords.csv')
LAST_WORDS_CLEANED_PATH = os.path.join(DATA_PATH, 'lastwords_cleaned.csv')


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('utf-8')

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield row


def clean():
    with open(LAST_WORDS_PATH) as data_file:
        reader = DictReader(data_file)
        valid_statements = [
            r for r in reader if r['words'] != 'This offender declined to make a last statement.'
        ]
        with open(LAST_WORDS_CLEANED_PATH) as cleaned_data_file:
            writer = csv.DictWriter(cleaned_data_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(valid_statements)

def get_formatted_entries(entry):
    full_text = 'Death row quote of the day:\n{} {}, Age: {}\n\n{}'.format(
        entry['first name'],
        entry['last name'],
        entry['age'],
        entry['words']
    )
    scanner = Scanner(full_text)
    return [line for line in scanner]

def get_tweets():
    with open(LAST_WORDS_CLEANED_PATH) as data_file:
        entry_idx = random.randint(1, 405)
        reader = DictReader(data_file)
        for idx, entry in enumerate(reader):
            if idx == entry_idx:
                return reversed(get_formatted_entries(entry))


class Scanner(object):
    def __init__(self, text):
        self.text = text
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx > len(self.text):
            raise StopIteration()
        return_text = self.text[self.idx:self.idx + 140]
        self.idx += 140
        return return_text
