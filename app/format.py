import decimal

def format_number(number, locale):
    if not isinstance(number, decimal.Decimal):
        number = 0.0
    if locale == "pt-br":
        result = str(number).replace(".", ",")
        if result.find(',') == -1:
            result = result + ",00"
        return result
    return "{0:.2f}".format(number)
