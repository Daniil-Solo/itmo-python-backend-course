from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db_session
from courses.services import CourseService, StudentChoiceService
from courses.repositories import (
    SQLAlchemyCourseRepository, SQLAlchemyStudentRepository, SQLAlchemySemesterPlanRepository
)


def get_course_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CourseService:
    """
    Возвращает сервис для работы с курсами
    """
    course_repo = SQLAlchemyCourseRepository(session)
    return CourseService(course_repo)


def get_choice_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> StudentChoiceService:
    """
    Возвращает сервис для работы с выбором курсов
    """
    semester_plan_repo = SQLAlchemySemesterPlanRepository(session)
    student_repo = SQLAlchemyStudentRepository(session)
    course_repo = SQLAlchemyCourseRepository(session)
    return StudentChoiceService(semester_plan_repo, student_repo, course_repo)
