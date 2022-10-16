TRUTHY = ["s", "sim", "y", "yes", "True", "t", "true"]
FALSY = ["n", "nao", "não", "no", "False", "f", "false"]


class Bool:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        value = str(v).lower()
        if value in TRUTHY:
            return True
        if value in FALSY:
            return False
        return bool(v)
