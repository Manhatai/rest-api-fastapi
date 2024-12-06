from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.bookings.bookings_schema import BookingSchema
from infra.sql.bookings.bookings_model import BookingsTable

bookings_router = APIRouter()

@bookings_router.get("/bookings", response_model=list[BookingSchema], status_code=200)
async def read_tasks(db: Session = Depends(get_db)):
    all_bookings = db.query(BookingsTable).all()
    return all_bookings

@bookings_router.get("/bookings/{booking_id}", response_model=BookingSchema, status_code=200)
async def read_task(booking_id: int):
    for booking in bookings:
        if booking.id == booking_id:
            return booking
        raise HTTPException(status_code=404, detail="The following booking doesn't exist!")
    
@bookings_router.post("/bookings", response_model=BookingSchema, status_code=201)
async def create_task(booking: BookingSchema, db: Session = Depends(get_db)):
    new_client = ClientsTable( # constructor
        firstName = client.firstName,
        phone = client.phone
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
            
@bookings_router.put("/bookings/{booking_id}", response_model=BookingSchema, status_code=200)
async def update_task(booking_id: int, task_updated: BookingSchema):
    for booking in bookings:
        if booking.id == booking_id:
            for key, value in task_updated:
                setattr(booking, key, value)
            return booking
        raise HTTPException(status_code=404, detail="The following booking doesn't exist!")        
            
@bookings_router.delete("/bookings/{booking_id}", status_code=204)
async def delete_task(booking_id: int):
    for booking in bookings:
        if booking.id == booking_id:
            bookings.remove(booking)
            return ''
        raise HTTPException(status_code=404, detail="The following booking doesn't exist!")  
