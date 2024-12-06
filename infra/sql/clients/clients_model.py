from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infra.sql.database.database import Base

class ClientsTable(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(String(32), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    bookings: Mapped["BookingsTable"] = relationship(back_populates='client')  # type: ignore