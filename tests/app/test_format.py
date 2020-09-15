from decimal import Decimal
from app.format import format_number

class TestFormatNumber:
    def test_not_a_number(self):
        assert format_number("10", None) == "0.00"

    def test_default(self):
        assert format_number(Decimal(10.0), None) == "10.00"

    def test_en_us(self):
        assert format_number(Decimal(10.0), 'en-us') == "10.00"

    def test_pt_br(self):
        assert format_number(Decimal(10.0), 'pt-br') == "10,00"
