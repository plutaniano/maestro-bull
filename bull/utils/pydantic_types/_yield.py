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
        if match := IPCA_PLUS.match(v):
            linear, angular = "ipca", None
        elif match := CDI_PLUS.match(v):
            linear, angular = "cdi", None
        elif match := IPCA.match(v):
            linear, angular = None, "ipca"
        elif match := CDI.match(v):
            linear, angular = None, "cdi"
        elif match := PERCENT.match(v):
            linear, angular = None, None
        percent = match.group("percent")
        # return {
        #     "percent": float(percent.replace(",", ".")),
        #     "linear": linear,
        #     "angular": angular,
        # }
        return float(percent.replace(",", "."))
