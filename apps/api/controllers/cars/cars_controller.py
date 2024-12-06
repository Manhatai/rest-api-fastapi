from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.cars.cars_schema import Car
from infra.sql.cars.cars_model import CarsTable
from typing import List

cars_router = APIRouter()
cars = []

@cars_router.post("/cars", response_model=Car, status_code=201)
async def create_task(car: Car):
    cars.append(car)
    return car
    

@cars_router.get("/cars", response_model=List[Car], status_code=200)
async def read_tasks(db: Session = Depends(get_db)):
    all_cars = db.query(CarsTable).all()
    return all_cars

@cars_router.get("/cars/{car_id}", response_model=Car, status_code=200)
async def read_task(car_id: int):
    for car in cars:
        if car.id == car_id:
            return car
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")
            
@cars_router.put("/cars/{car_id}", response_model=Car, status_code=200)
async def update_task(car_id: int, task_updated: Car):
    for car in cars:
        if car.id == car_id:
            for key, value in task_updated:
                setattr(car, key, value)
            return car
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")        
            
@cars_router.delete("/cars/{car_id}", status_code=204)
async def delete_task(car_id: int):
    for car in cars:
        if car.id == car_id:
            cars.remove(car)
            return ''
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")  
