from django.db.models import TextChoices


class Suitability(TextChoices):
    AGGRESSIVE = "aggressive", "Agressivo"
    MODERATE = "moderate", "Moderado"
    CONSERVATIVE = "conservative", "Conservador"
    OUT_OF_DATE = "out_of_date", "Desatualizado"
    NOT_FILLED = "not_filled", "Não preenchido"


class InvestorQualification(TextChoices):
    REGULAR = "regular", "Regular"
    QUALIFIED = "qualified", "Qualificado"
    PROFESSIONAL = "professional", "Profissional"
