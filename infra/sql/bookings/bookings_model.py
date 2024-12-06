from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infra.sql.database.database import Base

class BookingsTable(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(32), nullable=False)
    hour: Mapped[str] = mapped_column(String(32), nullable=False)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey('cars.id'), nullable=False)
    car: Mapped["CarsTable"] = relationship(back_populates='bookings') # type: ignore
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    client: Mapped["ClientsTable"] = relationship(back_populates='bookings') # type: ignore