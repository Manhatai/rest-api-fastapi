from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infra.sql.database.database import Base
#from infra.sql.bookings.bookings_model import BookingsTable

class CarsTable(Base):
    __tablename__ = 'cars'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(32), nullable=False)
    model: Mapped[str] = mapped_column(String(32), nullable=False)
    year: Mapped[str] = mapped_column(String(32), nullable=False)
    malfunction: Mapped[str] = mapped_column(String(64), nullable=False)
    bookings: Mapped["BookingsTable"] = relationship(back_populates='car')