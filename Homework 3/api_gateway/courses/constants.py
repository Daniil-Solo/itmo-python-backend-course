from enum import Enum


class Role(str, Enum):
    """
    Роль в проекте, на которую рассчитан курс
    """
    DE = 'Data Engineer'
    MLE = 'ML Engineer'
    DA = 'Data Analyst'
    A = 'AI Architect'


class Implementer(str, Enum):
    """
    Реализатор курса
    """
    IPKN = 'ИПКН'
    PISH = 'ПИШ'
    WSH_CK = 'ВШ ЦК'
