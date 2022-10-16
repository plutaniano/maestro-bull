from django.db.models import TextChoices


class Sex(TextChoices):
    M = "m", "Masculino"
    F = "f", "Feminino"


class Branches(TextChoices):
    SJC = "sao_jose_dos_campos", "São José dos Campos"
    SAO_PAULO = "sao_paulo", "São Paulo"
    PALMAS = "palmas", "Palmas"
    ALFENAS = "alfenas", "Alfenas"


class Classification(TextChoices):
    REVENUE = "revenue", "Receitas"
    ADJUSTMENT = "adjustment", "Ajustes"


class Insurers(TextChoices):
    ICATU = "icatu", "Icatu"
    METLIFE = "metlife", "Metlife"
    MONGERAL_AEGON = "mongeral_aegon", "Mongeral Aegon"
    OMINT = "omint", "Omint"
    PRUDENTIAL = "prudential", "Prudential"
    SULAMERICA = "sulamerica", "Sulamerica"
    XP = "xp", "XP"
    ZURICH = "zurich", "Zurich"


class State(TextChoices):
    AC = "ac", "Acre"
    AL = "al", "Alagoas"
    AM = "am", "Amazonas"
    AP = "ap", "Amapá"
    BA = "ba", "Bahia"
    CE = "ce", "Ceará"
    DF = "df", "Distrito Federal"
    ES = "es", "Espírito Santo"
    GO = "go", "Goiás"
    MA = "ma", "Maranhão"
    MG = "mg", "Minas Gerais"
    MS = "ms", "Mato Grosso do Sul"
    MT = "mt", "Mato Grosso"
    PA = "pa", "Pará"
    PB = "pb", "Paraíba"
    PE = "pe", "Pernambuco"
    PI = "pi", "Piauí"
    PR = "pr", "Paraná"
    RJ = "rj", "Rio de Janeiro"
    RN = "rn", "Rio Grande do Norte"
    RO = "ro", "Rondônia"
    RR = "rr", "Roraima"
    RS = "rs", "Rio Grande do Sul"
    SC = "sc", "Santa Catarina"
    SE = "se", "Sergipe"
    SP = "sp", "São Paulo"
    TO = "to", "Tocantins"
