from bull.core.exceptions import MaestroException


class XpApiException(MaestroException):
    """Erros relacionados à API da XP deverão herdar dessa classe."""


class TreasureNotEnabled(XpApiException):
    """Cliente não está habilitado para operar Tesouro. Provavelmente
    é uma segunda conta. (Só é permitida uma conta no Tesouro por CPF)"""
