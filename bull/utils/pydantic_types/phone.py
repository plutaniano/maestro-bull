from phonenumbers import (
    parse,
    PhoneNumberFormat,
    is_valid_number,
    format_number,
    NumberParseException,
)


class Phone(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.parse_number
        yield cls.validate
        yield cls.format

    @classmethod
    def parse_number(cls, v):
        try:
            return parse(v, "BR")
        except NumberParseException:
            raise ValueError(f"{v} does not seems to be a phone number")

    @classmethod
    def validate(cls, v):
        try:
            assert is_valid_number(v)
        except AssertionError:
            raise ValueError(f"{v} is not a valid phone number")
        return v

    @classmethod
    def format(cls, v):
        return format_number(v, PhoneNumberFormat.INTERNATIONAL)
