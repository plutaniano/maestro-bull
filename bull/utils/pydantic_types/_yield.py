import re

IPCA_PLUS = re.compile(r"IPC-A \+ (?P<percent>\d.*)%")
CDI_PLUS = re.compile(r"CDI \+ (?P<percent>\d.*)%")
CDI = re.compile(r"(?P<percent>\d.*)% CDI")
IPCA = re.compile(r"(?P<percent>\d.*)% IPCA")
PERCENT = re.compile(r"(?P<percent>\d.*)%")


class Yield:
    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def parse(cls, v):
        match = (
            IPCA_PLUS.match(v)
            or CDI_PLUS.match(v)
            or IPCA.match(v)
            or CDI.match(v)
            or PERCENT.match(v)
        )
        percent = match.group("percent")
        return float(percent.replace(",", "."))
