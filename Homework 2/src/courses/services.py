from typing import Optional
from courses.exceptions import NoSuchCourseException, NoSuchStudentException, \
    SemesterPlanForSuchStudentExistsException, SemesterPlanForSuchStudentDoesntExistsException
from courses.schemas import CourseShort, CourseFull, SemesterPlanCreate, SemesterPlan, OperationResult
from courses.repositories import AbstractCourseRepository, AbstractSemesterPlanRepository, AbstractStudentRepository


class CourseService:
    """
    Сервис для получения информации о курсах
    """
    def __init__(self, course_repo: AbstractCourseRepository):
        self.course_repo = course_repo

    async def get_courses(
            self,
            implementer: Optional[str] = None,
            role: Optional[str] = None,
            search: Optional[str] = None
    ) -> list[CourseShort]:
        """
        Возвращает список курсов, удовлетворяющих фильтру
        :param implementer: Название реализатора курса
        :param role: Название роли для курса
        :param search: Часть названия курса
        :return: Список курсов
        """
        filtered_courses = await self.course_repo.list()
        if implementer is not None:
            filtered_courses = filter(lambda c: c.implementer == implementer, filtered_courses)
        if role is not None:
            filtered_courses = filter(lambda c: role in c.roles, filtered_courses)
        if search is not None:
            filtered_courses = filter(lambda c: search.lower() in c.name.lower(), filtered_courses)
        return [course.to_short() for course in filtered_courses]

    async def get_course_info(self, course_id: int) -> CourseFull:
        """
        Возвращает подробную информацию о куре (описание, роли, время занятий и т.д.) по его id
        :param course_id: идентификатор курса
        :return: подробная информация о курсе
        """
        course = await self.course_repo.one(course_id)
        if course is None:
            raise NoSuchCourseException("Курса с таким идентификатором не существует")
        return course


class StudentChoiceService:
    """
    Сервис для работы с выбором студента и формированием его план изучения дисциплин
    """
    def __init__(
            self,
            semester_plan_repo: AbstractSemesterPlanRepository,
            student_repo: AbstractStudentRepository,
            course_repo: AbstractCourseRepository
    ):
        self.semester_plan_repo = semester_plan_repo
        self.student_repo = student_repo
        self.course_repo = course_repo

    async def get_plan(self, student_id: int) -> SemesterPlan:
        """
        Возвращает план для изучения дисциплин студента
        :param student_id: идентификатор студента
        :return: план для изучения дисциплин
        """
        if not await self.student_repo.exists(student_id):
            raise NoSuchStudentException("Студента с таким идентификатором не существует")
        plan = await self.semester_plan_repo.one(student_id)
        if plan is None:
            raise SemesterPlanForSuchStudentDoesntExistsException(
                "План изучения дисциплин на семестр для данного студента ещё не создан"
            )
        return plan

    async def create_plan(self, student_id: int, semester_plan_data: SemesterPlanCreate) -> SemesterPlan:
        """
        Создает план изучения дисциплин на семестр для студента
        :param student_id: идентификатор студента
        :param semester_plan_data: информация о семестре (нагрузка)
        :return: план изучения дисциплин на семестр
        """
        if not await self.student_repo.exists(student_id):
            raise NoSuchStudentException("Студента с таким идентификатором не существует")
        plan = await self.semester_plan_repo.one(student_id)
        if plan is not None:
            raise SemesterPlanForSuchStudentExistsException(
                "План изучения дисциплин на семестр для данного студента уже существует"
            )
        semester_plan = await self.semester_plan_repo.add_one(student_id, semester_plan_data)
        return semester_plan

    @staticmethod
    def has_time_for_course(current_courses: list[CourseFull], adding_course: CourseFull) -> bool:
        """
        Проверяет, есть ли занятия в курсах плана и добавляемом курсе, которые будут пересекаться во времени
        Считается, что одно занятие начинается строго в определенное время и не может заниматься больше
        2 пар (~3 часов)
        :param current_courses: существующие курсы в плане для изучения дисциплин
        :param adding_course: добавляемый курс
        :return: удастся ли выполнить добавление курса в план
        """
        current_lessons_set = set()
        new_lessons_set = set()
        for current_course in current_courses:
            for current_lesson in current_course.lessons:
                start_time, finish_time = current_lesson.string_time_interval.split(" - ")
                day = current_lesson.string_day
                current_lessons_set.add((day, start_time))
                current_lessons_set.add((day, finish_time))
        for new_lesson in adding_course.lessons:
            start_time, finish_time = new_lesson.string_time_interval.split(" - ")
            day = new_lesson.string_day
            new_lessons_set.add((day, start_time))
            new_lessons_set.add((day, finish_time))
        overlapping_lessons = current_lessons_set.intersection(new_lessons_set)
        return len(overlapping_lessons) == 0

    async def check_course_for_semester_plan(self, plan: SemesterPlan, adding_course: CourseFull) -> OperationResult:
        """
        Пробует добавить курс в план для изучения дисциплин
        :param plan: план для изучения дисциплин
        :param adding_course: добавляемый курс
        :return: результат операции
        """
        if adding_course.id in [c.id for c in plan.courses]:
            return OperationResult(is_successful=False, message="Курс уже включен в план для изучения")
        if len(plan.courses) == plan.semester_load:
            return OperationResult(is_successful=False, message="Достигнут предел по учебной нагрузке")
        if adding_course.is_prerecorded_course:
            await self.semester_plan_repo.add_course(adding_course.id, plan.id)
            return OperationResult(is_successful=True, message="Курс успешно добавлен")
        current_courses = [await self.course_repo.one(c.id) for c in plan.courses]
        if self.has_time_for_course(current_courses, adding_course):
            await self.semester_plan_repo.add_course(adding_course.id, plan.id)
            return OperationResult(is_successful=True, message="Курс успешно добавлен")
        return OperationResult(is_successful=False, message="Данный курс пересекается с другими курсами")

    async def add_course(self, student_id: int, course_id: int) -> OperationResult:
        """
        Добавляет курс в плана изучения дисциплин студента
        :param student_id: идентификатор студента
        :param course_id: идентификатор курса
        :return: результат операции
        :return:
        """
        plan = await self.get_plan(student_id)
        if plan.is_confirmed:
            return OperationResult(is_successful=False, message="План уже подтвержден и не может быть изменен")
        course = await self.course_repo.one(course_id)
        if course is None:
            raise NoSuchCourseException("Курса с таким идентификатором не существует")
        operation_result = await self.check_course_for_semester_plan(plan, course)
        return operation_result

    async def remove_course(self, student_id: int, course_id: int) -> OperationResult:
        """
        Удаляет курс из плана изучения дисциплин студента
        :param student_id: идентификатор студента
        :param course_id: идентификатор курса
        :return: результат операции
        """
        plan = await self.get_plan(student_id)
        if plan.is_confirmed:
            return OperationResult(is_successful=False, message="План уже подтвержден и не может быть изменен")
        course = await self.course_repo.one(course_id)
        if course is None:
            raise NoSuchCourseException("Курса с таким идентификатором не существует")
        await self.semester_plan_repo.remove_course(course.id, plan.id)
        return OperationResult(is_successful=True, message="Курс успешно удален из плана")

    async def confirm_plan(self, student_id: int) -> OperationResult:
        """
        Подтверждает план изучения дисциплин для студента
        :param student_id: идентификатор студента
        :return: результат операции
        """
        plan = await self.get_plan(student_id)
        if plan.is_confirmed:
            return OperationResult(is_successful=False, message="План уже подтвержден")
        if len(plan.courses) < plan.semester_load:
            return OperationResult(
                is_successful=False,
                message=f"Выбрано недостаточно курсов. Нужно добавить ещё {plan.semester_load-len(plan.courses)}"
            )
        await self.semester_plan_repo.update(plan.id, is_confirmed=True)
        return OperationResult(is_successful=True, message="План изучения дисциплин успешно подтвержден")
