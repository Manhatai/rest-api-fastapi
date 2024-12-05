from fastapi import APIRouter, HTTPException
from infra.sql.database.database import cars
from infra.schemas.cars.cars_schema import Car
from typing import List

cars_router = APIRouter()

@cars_router.post("/", response_model=Car, status_code=201)
async def create_task(car: Car):
    cars.append(car)
    return car
    

@cars_router.get("/", response_model=List[Car], status_code=200)
async def read_tasks():
    return cars

@cars_router.get("/{car_id}", response_model=Car, status_code=200)
async def read_task(car_id: int):
    for car in cars:
        if car.id == car_id:
            return car
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")
            
@cars_router.put("/{car_id}", response_model=Car, status_code=200)
async def update_task(car_id: int, task_updated: Car):
    for car in cars:
        if car.id == car_id:
            for key, value in task_updated:
                setattr(car, key, value)
            return car
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")        
            
@cars_router.delete("/{car_id}", status_code=204)
async def delete_task(car_id: int):
    for car in cars:
        if car.id == car_id:
            cars.remove(car)
            return ''
        raise HTTPException(status_code=404, detail="The following car doesn't exist!")  
