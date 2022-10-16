from decimal import Decimal


class Money(Decimal):
    @classmethod
    def __get_validators__(cls):
        yield cls.remove_formatting
        yield cls.to_decimal

    @classmethod
    def remove_formatting(cls, v):
        v = str(v)
        if "." in v[-3:]:
            # "1,234,567.89" -> "1234567.89"
            v = v.replace(",", "")
        elif "," in v[-3:]:
            # "1.234.567,89" -> "1234567.89"
            v = v.replace(".", "").replace(",", ".")
        return v

    @classmethod
    def to_decimal(cls, v):
        return Decimal(v).quantize(Decimal("0.00"))
