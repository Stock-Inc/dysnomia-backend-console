from sqlalchemy.types import Integer, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class ConsoleCommand(Base):
    __tablename__ = 'console'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True, name='command')
    description: Mapped[str] = mapped_column(VARCHAR(255))
    result: Mapped[str] = mapped_column(VARCHAR(255))
