from datetime import date, datetime

from dateutil import parser
from pydantic import PydanticValueError


class CantParseDate(PydanticValueError):
    code = "cant_parse_date"
    msg_template = "can't parse '{value}' as date"


class Date(date):
    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def parse(cls, v):
        if isinstance(v, date):
            return v
        if isinstance(v, datetime):
            return v.date()
        try:
            return parser.parse(v).date()
        except Exception:
            raise CantParseDate(value=v)
