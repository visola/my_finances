from decimal import Decimal
from datetime import date
from datetime import datetime
from app.locale_format import format_number
from app.locale_format import format_currency
from app.locale_format import format_date

class TestFormatNumber:
    def test_not_a_number(self):
        assert format_number("10", None) == "0.00"

    def test_default(self):
        assert format_number(Decimal(10.0), None) == "10.00"

    def test_en_us(self):
        assert format_number(Decimal(10.0), 'en-us') == "10.00"

    def test_pt_br(self):
        assert format_number(Decimal(10.0), 'pt-br') == "10,00"

class TestFormatCurrency:
    def test_not_a_number(self):
        assert format_currency("10", None) == "$ 0.00"

    def test_default(self):
        assert format_currency(Decimal(10.0), None) == "$ 10.00"

    def test_en_us(self):
        assert format_currency(Decimal(10.0), 'en-us') == "$ 10.00"

    def test_pt_br(self):
        assert format_currency(Decimal(10.0), 'pt-br') == "R$ 10,00"

class TestFormatDate:
    def test_default(self):
        assert format_date(datetime(1999,12,21), None) == "12/21/1999"

    def test_en_us(self):
        assert format_date(datetime(1999,12,21), 'en-us') == "12/21/1999"
    
    def test_pt_br(self):
        assert format_date(datetime(1999,12,21), 'pt-br') == "21/12/1999"
