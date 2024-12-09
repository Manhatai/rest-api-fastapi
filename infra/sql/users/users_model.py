from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from infra.sql.database.database import Base

class UsersTable(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)