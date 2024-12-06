from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.bookings.bookings_schema import BookingSchema
from infra.sql.bookings.bookings_model import BookingsTable
from infra.sql.clients.clients_model import ClientsTable
from infra.sql.cars.cars_model import CarsTable

bookings_router = APIRouter()

@bookings_router.get("/bookings", response_model=list[BookingSchema], status_code=200)
async def get_bookings(db: Session = Depends(get_db)):
    all_bookings = db.query(BookingsTable).all()
    return all_bookings

@bookings_router.get("/bookings/{booking_id}", response_model=BookingSchema, status_code=200)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    specific_booking = db.query(BookingsTable).filter(BookingsTable.id == booking_id).first()
    if not specific_booking:
        raise HTTPException(status_code=404, detail="The following booking doesn't exist!")
    return specific_booking
    
@bookings_router.post("/bookings", response_model=BookingSchema, status_code=201)
async def create_booking(booking: BookingSchema, db: Session = Depends(get_db)):
    new_booking = BookingsTable( # constructor
        date = booking.date,
        hour = booking.hour,
        car_id = booking.car_id,
        client_id = booking.client_id
    )
    car = db.query(CarsTable).filter(CarsTable.id == booking.car_id).first()
    if car == None:
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")
    
    client = db.query(ClientsTable).filter(ClientsTable.id == booking.client_id).first()
    if client == None:
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking
            
@bookings_router.put("/bookings/{booking_id}", response_model=BookingSchema, status_code=200)
async def update_booking(booking_id: int, update_data: BookingSchema, db: Session = Depends(get_db)):
    booking = db.query(BookingsTable).filter(BookingsTable.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="The following booking doesn't exist!") 
    for key, value in update_data.model_dump(exclude_unset=True).items(): # .items() for value pairs
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return booking          
            
@bookings_router.delete("/bookings/{booking_id}", status_code=204)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    deleted_booking = db.query(BookingsTable).filter(BookingsTable.id == booking_id).first()
    if not deleted_booking:
        raise HTTPException(status_code=404, detail="The following booking doesn't exist!")  
    db.delete(deleted_booking)
    db.commit()
    return ''
