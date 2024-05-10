from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# Voor wachtwoorden
import bcrypt


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    password_hash = mapped_column(String)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'),
                                           bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),
                              self.password_hash)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}"

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_adress: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_adress={self.email_adress!r})"


class TodoList(Base):
    __tablename__ = "todolist"

    id: Mapped[int] = mapped_column(primary_key=True)

    todo_text: Mapped[str] = mapped_column(String(1000))
    todo_made_time = mapped_column(DateTime)
    todo_date = mapped_column(DateTime)
    todo_date_overdue = mapped_column(Boolean)
    todo_done = mapped_column(Boolean)

    user_id = mapped_column(Integer)

    def __repr__(self):
        return (f"TodoList(id={self.id!r},"
                f"todo_text={self.todo_text!r},"
                f"user_id={self.user_id!r}, "
                f"todo_made_time={self.todo_made_time!r}, "
                f"todo_date={self.todo_date},"
                f"todo_date_overdue={self.todo_date_overdue},"
                f"todo_done={self.todo_done})")