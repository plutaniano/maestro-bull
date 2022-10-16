class MaestroException(Exception):
    "Exception base do projeto. Todas as Exceptions deverão herdar desta classe."


class ParseError(MaestroException):
    def __init__(self, errors):
        self.errors = errors
