from sqlalchemy import Integer
import sqlalchemy.orm as so


class Base(so.DeclarativeBase):  # pylint: disable=too-few-public-methods
    """
    Базовый класс для моделей
    """
    id: so.Mapped[int] = so.mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
