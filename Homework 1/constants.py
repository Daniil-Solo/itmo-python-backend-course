from schemas import Course, Role, Implementer


COURSES = [
    Course(
        id=1,
        title="DevOps практики и инструменты",
        roles=[Role.DE, Role.MLE, Role.DA],
        implementer=Implementer.IPKN
    ),
    Course(
        id=2,
        title="Проектирование микросервисов",
        roles=[Role.A, Role.MLE],
        implementer=Implementer.IPKN
    ),
    Course(
        id=3,
        title="Хранение больших данных и Введение в МО (Python)",
        roles=[Role.DE, Role.MLE, Role.DA],
        implementer=Implementer.PISH
    ),
    Course(
        id=4,
        title="Создание технологического бизнеса",
        roles=[Role.PM],
        implementer=Implementer.OTHER
    ),
    Course(
        id=5,
        title="Управление данными",
        roles=[Role.PM, Role.DE],
        implementer=Implementer.IPKN
    ),
    Course(
        id=6,
        title="Разработка веб-приложений (Python Backend)",
        roles=[Role.MLE],
        implementer=Implementer.IPKN
    ),
]
