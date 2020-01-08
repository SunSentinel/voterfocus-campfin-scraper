import re
from re import sub
from decimal import Decimal
from datetime import datetime

"""
Utility functions for formatting scraped data
"""


def get_name(text):
    name = re.sub(r'\([^)]*\)', '', text)
    return name.strip()


def get_party(text):
    if "(DEM)" in text:
        return "Democrat"
    elif "(REP)" in text:
        return "Republican"
    else:
        return ""

def get_in_parenthesis(text):
    try:
        return re.search('\(([^)]+)', text).group(1)
    except:
        return ""


def strip_spaces(text):
    return text.strip()


def strip_breaks(text):
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = text.replace('\xa033606', '')
    text = text.replace('  ', ' ')
    text = text.replace('   ', ' ')
    re.sub(' +', ' ', text)
    return text.strip()


def toDate(text):
    text = text.strip()

    try:
        dt = datetime.strptime(text, '%m/%d/%Y')
        return dt.date().isoformat()

    except ValueError:
        return ''


def CashtoFloat(text):
    text = text.strip().replace("$", "").replace(",", "")
    return float(text)
    # return text