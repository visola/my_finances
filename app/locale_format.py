import decimal
from datetime import datetime

def format_number(number, locale):
    if not isinstance(number, decimal.Decimal):
        number = 0.0
    if locale == "pt-br":
        result = str(number).replace(".", ",")
        if result.find(',') == -1:
            result = result + ",00"
        return result
    return "{0:.2f}".format(number)

def format_currency(number, locale):
    if not isinstance(number, decimal.Decimal):
        number = 0.0
    if locale == "pt-br":
        result = str(number).replace(".", ",")
        if result.find(',') == -1:
            result = result + ",00"
        return "R$ " + result
    return "$ {0:.2f}".format(number)

def format_date(to_format, locale):
    if locale == "pt-br":
        return datetime.strftime(to_format, '%d/%m/%Y')
    return datetime.strftime(to_format, '%m/%d/%Y')
