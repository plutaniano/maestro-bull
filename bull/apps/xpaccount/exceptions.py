from bull.core.exceptions import MaestroException


class ValidCookieNotAvailable(MaestroException):
    "Não existe um cookie válido."


class XPAccountIsInactive(MaestroException):
    "Cliente está inativo."
