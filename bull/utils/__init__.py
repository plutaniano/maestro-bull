import zoneinfo
import decimal
from .shortcuts import get_object_or_none

BR_TZ = zoneinfo.ZoneInfo("America/Sao_Paulo")


def zero_div(dividend, divisor, default=None):
    try:
        return dividend / divisor
    except (ZeroDivisionError, decimal.InvalidOperation) as e:
        return default
