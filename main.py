from fastapi import FastAPI
from apps.api.controllers.clients.clients_controller import clients_router
from apps.api.controllers.cars.cars_controller import cars_router
from apps.api.controllers.bookings.bookings_controller import bookings_router
from infra.sql.database.database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CMWSApi"
) 

app.include_router(clients_router, prefix="/api")
app.include_router(cars_router, prefix="/api")
app.include_router(bookings_router, prefix="/api")

# import uvicorn
#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8080) # or localhost