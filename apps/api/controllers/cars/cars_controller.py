from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.cars.cars_schema import CarSchema
from infra.sql.cars.cars_model import CarsTable

cars_router = APIRouter()

@cars_router.get("/cars", response_model=list[CarSchema], status_code=200)
async def get_cars(db: Session = Depends(get_db)):
    all_cars = db.query(CarsTable).all()
    return all_cars

@cars_router.get("/cars/{car_id}", response_model=CarSchema, status_code=200)
async def get_car(car_id: int, db: Session = Depends(get_db)):
    specific_car = db.query(CarsTable).filter(CarsTable.id == car_id).first()
    if not specific_car:
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")
    return specific_car
    
@cars_router.post("/cars", response_model=CarSchema, status_code=201)
async def create_car(car: CarSchema, db: Session = Depends(get_db)):
    new_car = CarsTable(
        brand = car.brand,
        model = car.model,
        year = car.year,
        malfunction = car.malfunction
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car
            
@cars_router.put("/cars/{car_id}", response_model=CarSchema, status_code=200)
async def update_car(car_id: int, update_data: CarSchema, db: Session = Depends(get_db)):
    car = db.query(CarsTable).filter(CarsTable.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="The following car doesn't exist!") 
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return car        
            
@cars_router.delete("/cars/{car_id}", status_code=204)
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    deleted_car = db.query(CarsTable).filter(CarsTable.id == car_id).first()
    if not deleted_car:
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")  
    db.delete(deleted_car)
    db.commit()
    return ''
