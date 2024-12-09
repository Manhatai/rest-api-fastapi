from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.cars.cars_schema import CarSchema
from infra.sql.cars.cars_model import CarsTable
from infra.sql.bookings.bookings_model import BookingsTable
from utils.global_catch.global_catch import global_catch
from utils.auth_check.auth_check import TokenBearer
from utils.logger.logger import logger

cars_router = APIRouter()
token_bearer = TokenBearer()

@cars_router.get("/cars", response_model=list[CarSchema], status_code=200)
@global_catch
async def get_cars(db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    all_cars = db.query(CarsTable).all()
    logger.info(f"Car list returned successfully. [200]")
    return all_cars

@cars_router.get("/cars/{car_id}", response_model=CarSchema, status_code=200)
@global_catch
async def get_car(car_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    specific_car = db.query(CarsTable).filter(CarsTable.id == car_id).first()
    if not specific_car:
        logger.info(f"Car with ID {car_id} not found. [404]")
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")
    logger.info(f"GET request for client ID {car_id} successfull. [200]")
    return specific_car
    
@cars_router.post("/cars", response_model=CarSchema, status_code=201)
@global_catch
async def create_car(car: CarSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    new_car = CarsTable(
        brand = car.brand,
        model = car.model,
        year = car.year,
        malfunction = car.malfunction
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    logger.info(f"POST request for car ID {new_car.id} successfull. [200]")
    return new_car
            
@cars_router.put("/cars/{car_id}", response_model=CarSchema, status_code=200)
@global_catch
async def update_car(car_id: int, update_data: CarSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    car = db.query(CarsTable).filter(CarsTable.id == car_id).first()
    if not car:
        logger.info(f"Car with ID {car_id} not found. [404]")
        raise HTTPException(status_code=404, detail="The following car doesn't exist!") 
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    logger.info(f"PUT request for car ID {car_id} successfull. [200]")
    return car        
            
@cars_router.delete("/cars/{car_id}", status_code=204)
@global_catch
async def delete_car(car_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    deleted_car = db.query(CarsTable).filter(CarsTable.id == car_id).first()
    if not deleted_car:
        logger.info(f"Car with ID {car_id} not found. [404]")
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")
    booking_check = db.query(BookingsTable).filter(car_id == car_id).first()
    if booking_check != None:
        logger.info(f"Car {car_id} has a booking history. Deletion unsuccessfull. [409]")
        raise HTTPException(status_code=409, detail="The following has booking history.")   
    db.delete(deleted_car)
    db.commit()
    logger.info(f"DELETE request for car ID {car_id} successfull. [204]")
    return ''
