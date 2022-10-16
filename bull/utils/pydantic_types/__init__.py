from pydantic import constr

from ._yield import Yield
from .advisor import Advisor
from .bool import Bool
from .cpf_cnpj import CNPJ, CPF
from .date import Date
from .force import Force
from .money import Money
from .phone import Phone

HexStr = constr(regex=r"^[a-f0-9]{64}$")
