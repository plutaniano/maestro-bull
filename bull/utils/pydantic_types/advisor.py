import re

from django.apps import apps
from pydantic import PydanticValueError


class AdvisorDoesNotExist(PydanticValueError):
    code = "advisor_does_not_exist"
    msg_template = 'Advisor with advisor_id "{advisor_id}" does not exist.'


class Advisor:
    @classmethod
    def __get_validators__(cls):
        yield cls.to_int
        yield cls.validate_exists

    @classmethod
    def to_int(cls, v):
        match v:
            case int() | float():
                return v
            case str():
                result = re.search(r"(\d{4,5})", v)
                if not result:
                    raise ValueError("invalid advisor string format")
                return int(result.group(1))
            case _:
                raise TypeError("value must be int or str")

    @classmethod
    def validate_exists(cls, v):
        if v == 0:
            return None
        try:
            return apps.get_model("user", "User").objects.get(advisor_id=v)
        except apps.get_model("user", "User").DoesNotExist:
            raise AdvisorDoesNotExist(advisor_id=v)
