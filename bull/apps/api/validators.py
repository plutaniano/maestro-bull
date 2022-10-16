from pydantic import BaseModel, root_validator, Field
from bull.utils.pydantic_types import Date
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def last_month():
    return timezone.localdate().replace(day=1)


def one_year_ago():
    return last_month() - relativedelta(years=1)


class DateRangeParams(BaseModel):
    start: Date = Field(default_factory=one_year_ago)
    end: Date = Field(default_factory=last_month)

    @root_validator
    def validate(cls, values):
        assert values["start"] <= values["end"]
        return values
