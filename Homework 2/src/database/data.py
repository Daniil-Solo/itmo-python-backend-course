from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from database.base import Base
from database.db import DBSession, engine
from courses.models import Implementer, Role, Course, Student, CourseLesson
from config import TEST_MODE


async def migrate() -> None:
    """
    Выполняет создание таблиц
    Для тестового режима сначала выполняется удаление таблиц
    """
    async with engine.begin() as conn:
        if TEST_MODE:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_students(session: AsyncSession) -> None:
    """
    Создает в БД студентов
    :param session: сессия БД
    """
    student_1 = Student(firstname="Иван", lastname="Иванов")
    student_2 = Student(firstname="Петр", lastname="Петров")
    student_3 = Student(firstname="Тест", lastname="Тестовый")
    students = [student_1, student_2, student_3]
    session.add_all(students)
    await session.commit()


async def create_roles(session: AsyncSession) -> dict[str:Role]:
    """
    Создает в БД роли для курсов
    :param session: сессия БД
    :return: словарь вида "Название роли": "Объект модели Роли"
    """
    role_mle = Role(name="ML Engineer")
    role_aia = Role(name="AI Architect")
    role_da = Role(name="Data Analyst")
    role_de = Role(name="Data Engineer")
    roles = [role_mle, role_aia, role_da, role_de]
    session.add_all(roles)
    await session.commit()
    for role in roles:
        await session.refresh(role)
    return {role.name: role for role in roles}


async def create_implementers(session: AsyncSession) -> dict[str:Implementer]:
    """
    Создает в БД реализаторы для курсов
    :param session: сессия БД
    :return: словарь вида "Название реализатора": "Объект модели Реализатора"
    """
    imp_ipkn = Implementer(name="ИПКН")
    imp_pish = Implementer(name="ПИШ")
    imp_wsh_ck = Implementer(name="ВШ ЦК")
    implementers = [imp_ipkn, imp_pish, imp_wsh_ck]
    session.add_all(implementers)
    await session.commit()
    for implementer in implementers:
        await session.refresh(implementer)
    return {imp.name: imp for imp in implementers}


async def create_courses(  # pylint: disable=too-many-locals,too-many-branches
        session: AsyncSession,
        roles: dict[str:Role],
        implementers: dict[str:Implementer]
) -> list[Course]:
    """
    Создает в БД курсы с указанием ролей
    :param session: сессия БД
    :param roles: словарь вида "Название роли": "Объект модели Роли"
    :param implementers: словарь вида "Название реализатора": "Объект модели Реализатора"
    :return: список объектов модели Курса
    """
    course_1 = Course(
        name="Хранение больших данных и Введение в МО (Python)",
        description="""\
Раздел "Хранение больших данных" научит организовывать хранение больших данных с помощью реляционных \
СУБД и NoSQL хранилищ. Изучаются методы проектирования структур данных, языки запросов к данным и приемы \
обработки структурированных и слабоструктурированных данных. Раздел "Введение в машинное обучение (Python)" \
знакомит слушателей с видами машинного обучения, демонстрирует практические примеры решения задач при помощи \
методов машинного обучения с использованием языка программирования Python. Основное внимание уделяется решению \
задач регрессии, задачам классификации и кластеризации.""",
        is_prerecorded_course=True,
        implementer=implementers["ВШ ЦК"]
    )
    course_2 = Course(
        name="Управление данными",
        description="""\
Курс охватывает различные аспекты, включая: извлечение, трансформацию и консолидацию данных, управление\
происхождением данных, их целостностью и качеством, инструментарий в работе с данными.\
Благодаря сочетанию теоретических знаний и практических упражнений слушатели получат четкое представление\
о дизайне архитектуры обработки данных, о методах управления данными на протяжении всего их жизненного цикла,\
а также о внедрении стратегии управления данными, соответствующей целям организации и нормативным требованиям.""",
        implementer=implementers["ИПКН"]
    )
    course_3 = Course(
        name="Стратегия развития AI-продуктов",
        description="""\
Курс направлен на получение навыков по разработке продуктовой стратегии - определению текущей ситуации бизнеса \
в целом и продукта в частности, определению целевого состояния, составления плана действий для достижения этого \
состояния и разработки комплекса мероприятий с контрольными точками и распределением этапов по датам. \
Рассматриваются темы составления ценностного предложения, вариации ценностного предложения, определения и валидации \
каналов продвижения, меры отстройки от конкурентов и комплекс мероприятий для составления плана дальнейшего развития \
продукта.""",
        implementer=implementers["ИПКН"]
    )
    course_4 = Course(
        name="Системы обработки и анализа больших массивов данных",
        description="""\
Курс посвящен изучению систем обработки и анализа больших массивов данных. В частности будет рассмотрена экосистема \
Hadoop, базовый фреймворк для работы с большими данными Spark, а также брокеры сообщений Apache Kafka и NoSQL БД \
Apache Cassandra. По итогам курса слушатель получит представление о ландшафте технологий больших данных, а также об \
их базовом внутреннем устройстве необходимым для работы с ними начальном в роли пользователя.""",
        implementer=implementers["ИПКН"]
    )
    course_5 = Course(
        name="Разработка веб-приложений (Python Backend)",
        description="""\
Глобальные задачи при разработке веб-приложений и их типы. Различные виды тестирования (функциональные: unit, \
integration, smoke, regression, системное; нефункциональное: нагрузочное тестирование), TDD, сравнение различных \
библиотек (pytest, unittest). Основные протоколы взаимодействия веб-приложений (REST (HTTP/1.0), gRPC, GraphQL, \
их достоинства и недостатки и применимость в тех или иных условиях. Разработка микросервисных веб-приложений, их \
размеры, преимущества и недостатки. Разработка микросервисных веб-приложений, их размеры, преимущества и недостатки. \
Нормализация баз данных, транзакционные принципы, кэширование (Redis). Развертывание веб-приложений и автоматизация \
(Docker, Jenkins, Kubernetes/OpenShift).""",
        implementer=implementers["ИПКН"]
    )
    course_6 = Course(
        name="Продвинутое МО (Python) и Глубокое обучение",
        description="""\
Раздел "Продвинутое машинное обучение(Python)" знакомит слушателей с методами снижения размерности набора признаков \
и методами факторного анализа. Рассматривается метод опорных векторов и деревья принятия решений, ансамбли моделей, \
а также еще одна ветка машинного обучения — обучение с подкреплением. Раздел "Глубокое обучение" знакомит слушателей \
с миром нейронных сетей. В ней обсуждаются отличия нейросетевого подхода от подхода классического машинного обучения, \
рассказывается про перцептрон, полносвязный нейронные сети, сверточные и рекуррентные архитектуры; обсуждается \
глубокое обучение с подкреплением, GANы, а также практические аспекты обучения: аугментация данных, тюнинг \
параметров, дропаут, оптимизация и многое другое.""",
        is_prerecorded_course=True,
        implementer=implementers["ВШ ЦК"]
    )
    course_7 = Course(
        name="Программирование на языке Kotlin",
        description="""\
Введение. Простейшие программы. Примитивные типы. Простые функции. Классы. Свойства. Перечисления. Итерирование. \
Исключения. Аргументы функций. Функции-расширения. Инфиксные вызовы. Наследование. Нетривиальные конструкторы. \
Дата-классы. Компаньоны. Система типов. Null в Kotlin. Коллекции. Функциональное API коллекций. Последовательности. \
Использование функциональных интерфейсов Java. Перегрузка операторов. Делегирование свойств. Фукнции высшего порядка. \
Инлайн-функции. Обобщенные типы. Аннотации и рефлексия. DSL. Корутины.""",
        implementer=implementers["ИПКН"]
    )
    course_8 = Course(
        name="Программирование на С++",
        description="""\
Введение. Дин.память. Области видимости, глобальные переменные, пространства имен. Заголовочные файлы. Классы \
Полиморфизм, RTTI, dynamic_cast, typeid. Шаблоны. Категории значений и мув семантика. Лямбды. STL функциональные \
объекты. Вариативные шаблоны. CTAD, CRTP. Error handling. Exceptions. Exception safety. Полиморфизм.""",
        is_prerecorded_course=True,
        implementer=implementers["ИПКН"]
    )
    course_9 = Course(
        name="Практикум по разработке ML-сервисов на Python",
        description="""\
Курс посвящен основам бекенда для ML разработчиков. Будут рассмотрены основы бекенд разработки, дизайна API, \
сервинга ML моделей и работа с базами данных. Библиотеки для WebUI на Python - dash и streamlit. Упаковка в Docker \
Сбор и анализ метрик.""",
        implementer=implementers["ПИШ"]
    )
    course_10 = Course(
        name="Параллельное программирование",
        description="""Онлайн-курс на платформе Stepik""",
        is_prerecorded_course=True,
        implementer=implementers["ИПКН"]
    )
    course_11 = Course(
        name="Основы построения рекомендательных систем",
        description="""\
В данном курсе рассказывается, как правильно поставить задачу, какие данные нужно собирать, освоите полезные приемы, \
попробуете популярные фреймворки для построения рекомендательных систем, создадите собственный прототип и узнаете, как \
довести его до продакшена. Также будут затронуты темы оценки эффекта влияния рекомендательной модели на продукт и \
способы измерения этого влияния, real-time микро сервисной архитектуры для рекомендательных сервисов, и, конечно, \
научимся использовать более сложные модели, а именно: двухуровневые и нейросетевые. Большая часть домашних заданий \
будет связаны с разработкой или улучшением рекомендательного сервиса на основе заданного шаблона. Но и про \
особенности локальной разработки, такие как ускорение расчета метрик или визуализация работы моделей в Jupyter \
Notebook, здесь также будет упомянуто.""",
        implementer=implementers["ИПКН"]
    )
    course_12 = Course(
        name="Алгоритмы и структуры данных",
        description="""\
В этом курсе мы рассмотрим основные алгоритмы и структуры данных, которые ДОЛЖЕН знать каждый программист. \
(хотя бы для того, чтобы проходить алгоритмические собеседования на leetcode) Мы покрываем базу: сортировки, стек, \
очередь, бинарные деревья поиска, динамическое программирование, строки и графы.""",
        implementer=implementers["ИПКН"]
    )
    courses = [
        course_1, course_2, course_3, course_4, course_5,
        course_6, course_7, course_8, course_9, course_10,
        course_11, course_12
    ]
    for role in [roles["ML Engineer"], roles["Data Engineer"], roles["Data Analyst"]]:
        course_1.roles.append(role)
    for role in [roles["Data Engineer"]]:
        course_2.roles.append(role)
    for role in [roles["AI Architect"]]:
        course_3.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Engineer"], roles["Data Analyst"]]:
        course_4.roles.append(role)
    for role in [roles["ML Engineer"]]:
        course_5.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Analyst"]]:
        course_6.roles.append(role)
    for role in [roles["ML Engineer"]]:
        course_7.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Engineer"]]:
        course_8.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Engineer"], roles["Data Analyst"], roles["AI Architect"]]:
        course_9.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Engineer"]]:
        course_10.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Analyst"], roles["AI Architect"]]:
        course_11.roles.append(role)
    for role in [roles["ML Engineer"], roles["Data Engineer"], roles["Data Analyst"]]:
        course_12.roles.append(role)
    session.add_all(courses)
    await session.commit()
    for course in courses:
        await session.refresh(course)
    return [course_2, course_3, course_4, course_5, course_7, course_9, course_11, course_12]


async def create_course_lessons(  # pylint: disable=too-many-locals
        session: AsyncSession,
        courses: list[Course]
) -> None:
    """
    Создает для курсов занятия
    :param session: сессия в БД
    :param courses: список объектов модели Курса
    """
    course_2, course_3, course_4, course_5, course_7, course_9, course_11, course_12 = courses
    course_2_lessons = [
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=10, day=30, hour=18, minute=40),
            finish_time=datetime(year=2023, month=10, day=30, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=2, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=2, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=2, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=2, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=6, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=6, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=9, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=9, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=13, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=13, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=16, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=16, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=20, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=20, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=23, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=23, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=27, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=27, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=11, day=30, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=30, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=4, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=4, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=11, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=11, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=18, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=18, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=21, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=21, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=25, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=25, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=28, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=28, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_2.id,
            start_time=datetime(year=2023, month=12, day=30, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=30, hour=20, minute=10)
        )
    ]

    course_3_lessons = [
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=9, day=25, hour=17, minute=0),
            finish_time=datetime(year=2023, month=9, day=25, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=9, day=30, hour=10, minute=0),
            finish_time=datetime(year=2023, month=9, day=30, hour=11, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=2, hour=17, minute=0),
            finish_time=datetime(year=2023, month=10, day=2, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=7, hour=10, minute=0),
            finish_time=datetime(year=2023, month=10, day=7, hour=11, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=9, hour=17, minute=0),
            finish_time=datetime(year=2023, month=10, day=9, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=14, hour=10, minute=0),
            finish_time=datetime(year=2023, month=10, day=14, hour=11, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=16, hour=17, minute=0),
            finish_time=datetime(year=2023, month=10, day=16, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=21, hour=10, minute=0),
            finish_time=datetime(year=2023, month=10, day=21, hour=11, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=23, hour=17, minute=0),
            finish_time=datetime(year=2023, month=10, day=23, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_3.id,
            start_time=datetime(year=2023, month=10, day=28, hour=11, minute=40),
            finish_time=datetime(year=2023, month=10, day=28, hour=13, minute=10)
        ),
    ]

    course_4_lessons = [
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=11, day=1, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=1, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=11, day=8, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=8, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=11, day=15, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=15, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=11, day=22, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=22, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=11, day=29, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=29, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=12, day=6, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=6, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=12, day=13, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=13, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=12, day=20, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=20, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_4.id,
            start_time=datetime(year=2023, month=12, day=27, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=27, hour=20, minute=10)
        ),
    ]

    course_5_lessons = [
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=9, day=26, hour=18, minute=40),
            finish_time=datetime(year=2023, month=9, day=26, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=10, day=3, hour=18, minute=40),
            finish_time=datetime(year=2023, month=10, day=3, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=10, day=10, hour=18, minute=40),
            finish_time=datetime(year=2023, month=10, day=10, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=10, day=17, hour=18, minute=40),
            finish_time=datetime(year=2023, month=10, day=17, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=10, day=24, hour=18, minute=40),
            finish_time=datetime(year=2023, month=10, day=24, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=10, day=31, hour=18, minute=40),
            finish_time=datetime(year=2023, month=10, day=31, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_5.id,
            start_time=datetime(year=2023, month=11, day=3, hour=18, minute=40),
            finish_time=datetime(year=2023, month=11, day=3, hour=20, minute=10)
        ),
    ]

    course_7_lessons = [
        CourseLesson(
            course_id=course_7.id,
            start_time=datetime(year=2023, month=9, day=25, hour=14, minute=40),
            finish_time=datetime(year=2023, month=9, day=25, hour=17, minute=40)
        ),
        CourseLesson(
            course_id=course_7.id,
            start_time=datetime(year=2023, month=10, day=2, hour=14, minute=40),
            finish_time=datetime(year=2023, month=10, day=2, hour=17, minute=40)
        ),
        CourseLesson(
            course_id=course_7.id,
            start_time=datetime(year=2023, month=10, day=9, hour=14, minute=40),
            finish_time=datetime(year=2023, month=10, day=9, hour=17, minute=40)
        ),
        CourseLesson(
            course_id=course_7.id,
            start_time=datetime(year=2023, month=10, day=16, hour=14, minute=40),
            finish_time=datetime(year=2023, month=10, day=16, hour=17, minute=40)
        ),
        CourseLesson(
            course_id=course_7.id,
            start_time=datetime(year=2023, month=10, day=23, hour=14, minute=40),
            finish_time=datetime(year=2023, month=10, day=23, hour=17, minute=40)
        ),
    ]

    course_9_lessons = [
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=7, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=7, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=10, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=10, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=14, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=14, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=17, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=17, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=21, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=21, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=24, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=24, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=11, day=28, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=28, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=12, day=1, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=1, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=12, day=8, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=8, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=12, day=15, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=15, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2023, month=12, day=22, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=22, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2024, month=1, day=10, hour=18, minute=40),
            finish_time=datetime(year=2024, month=1, day=10, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2024, month=1, day=11, hour=18, minute=40),
            finish_time=datetime(year=2024, month=1, day=11, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2024, month=1, day=17, hour=18, minute=40),
            finish_time=datetime(year=2024, month=1, day=17, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2024, month=1, day=18, hour=18, minute=40),
            finish_time=datetime(year=2024, month=1, day=18, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2024, month=1, day=24, hour=18, minute=40),
            finish_time=datetime(year=2024, month=1, day=24, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_9.id,
            start_time=datetime(year=2024, month=1, day=25, hour=18, minute=40),
            finish_time=datetime(year=2024, month=1, day=25, hour=20, minute=10)
        ),
    ]

    course_11_lessons = [
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=11, day=8, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=8, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=11, day=15, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=15, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=11, day=18, hour=11, minute=40),
            finish_time=datetime(year=2023, month=11, day=18, hour=13, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=11, day=22, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=22, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=11, day=25, hour=11, minute=40),
            finish_time=datetime(year=2023, month=11, day=25, hour=13, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=11, day=29, hour=17, minute=0),
            finish_time=datetime(year=2023, month=11, day=29, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=12, day=2, hour=11, minute=40),
            finish_time=datetime(year=2023, month=12, day=2, hour=13, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=12, day=6, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=6, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=12, day=13, hour=17, minute=0),
            finish_time=datetime(year=2023, month=12, day=13, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=12, day=16, hour=11, minute=40),
            finish_time=datetime(year=2023, month=12, day=16, hour=13, minute=10)
        ),
        CourseLesson(
            course_id=course_11.id,
            start_time=datetime(year=2023, month=12, day=23, hour=11, minute=40),
            finish_time=datetime(year=2023, month=12, day=23, hour=13, minute=10)
        ),
    ]

    course_12_lessons = [
        CourseLesson(
            course_id=course_12.id,
            start_time=datetime(year=2023, month=9, day=28, hour=18, minute=40),
            finish_time=datetime(year=2023, month=9, day=28, hour=20, minute=10)
        ),
        CourseLesson(
            course_id=course_12.id,
            start_time=datetime(year=2023, month=10, day=25, hour=17, minute=00),
            finish_time=datetime(year=2023, month=10, day=25, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_12.id,
            start_time=datetime(year=2023, month=11, day=30, hour=17, minute=00),
            finish_time=datetime(year=2023, month=11, day=30, hour=18, minute=30)
        ),
        CourseLesson(
            course_id=course_12.id,
            start_time=datetime(year=2023, month=12, day=27, hour=18, minute=40),
            finish_time=datetime(year=2023, month=12, day=27, hour=20, minute=10)
        ),
    ]
    session.add_all(course_2_lessons)
    session.add_all(course_3_lessons)
    session.add_all(course_4_lessons)
    session.add_all(course_5_lessons)
    session.add_all(course_7_lessons)
    session.add_all(course_9_lessons)
    session.add_all(course_11_lessons)
    session.add_all(course_12_lessons)
    await session.commit()


async def create_data() -> None:
    """
    Заполнение БД данными
    Используется для тестирования
    """
    session = DBSession()

    # Роли
    roles = await create_roles(session)

    # Реализаторы
    implementers = await create_implementers(session)

    # Студенты
    await create_students(session)

    # Курсы
    courses = await create_courses(session, roles, implementers)
    await create_course_lessons(session, courses)

    await session.close()
