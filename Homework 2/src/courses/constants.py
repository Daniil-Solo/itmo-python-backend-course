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


MONTH_MAPPING = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}
