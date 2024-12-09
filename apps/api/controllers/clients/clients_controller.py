from fastapi import APIRouter, HTTPException, Depends, Request
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.clients.clients_schema import ClientSchema
from infra.sql.clients.clients_model import ClientsTable
from infra.sql.bookings.bookings_model import BookingsTable
from utils.global_catch.global_catch import global_catch
from utils.auth_check.auth_check import TokenBearer
from utils.logger.logger import logger

clients_router = APIRouter()
token_bearer = TokenBearer()

@clients_router.get("/clients", response_model=list[ClientSchema], status_code=200)
@global_catch
async def get_clients(db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    #raise TypeError("Only integers are allowed") 
    all_clients = db.query(ClientsTable).all()
    logger.info(f"Client list returned successfully. [200]")
    return all_clients

@clients_router.get("/clients/{client_id}", response_model=ClientSchema, status_code=200)
@global_catch
async def get_client(client_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    specific_client = db.query(ClientsTable).filter(ClientsTable.id == client_id).first()
    if not specific_client:
        logger.info(f"Client with ID {client_id} not found. [404]")
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")
    logger.info(f"GET request for client ID {client_id} successfull. [200]")
    return specific_client

@clients_router.post("/clients", response_model=ClientSchema, status_code=201)
@global_catch
async def create_client(client: ClientSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    new_client = ClientsTable( # constructor
        firstName = client.firstName,
        phone = client.phone
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    logger.info(f"POST request for client ID {new_client.id} successfull. [200]")
    return new_client

@clients_router.put("/clients/{client_id}", response_model=ClientSchema, status_code=200)
@global_catch
async def update_client(client_id: int, update_data: ClientSchema, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    client = db.query(ClientsTable).filter(ClientsTable.id == client_id).first()
    if not client:
        logger.info(f"Client with ID {client_id} not found. [404]")
        raise HTTPException(status_code=404, detail="The following client doesn't exist!") 
    for key, value in update_data.model_dump(exclude_unset=True).items(): # .items() for value pairs
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    logger.info(f"PUT request for client ID {client_id} successfull. [200]")
    return client      
        
@clients_router.delete("/clients/{client_id}", status_code=204)
@global_catch
async def delete_client(client_id: int, db: Session = Depends(get_db), user_details=Depends(token_bearer)):
    deleted_client = db.query(ClientsTable).filter(ClientsTable.id == client_id).first()
    if not deleted_client:
        logger.info(f"Client with ID {client_id} not found. [404]")
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")  
    booking_check = db.query(BookingsTable).filter(client_id == client_id).first()
    if booking_check != None:
        logger.info(f"Client {client_id} has a booking history. Deletion unsuccessfull. [409]")
        raise HTTPException(status_code=409, detail="The following has booking history.") 
    db.delete(deleted_client)
    db.commit()
    logger.info(f"DELETE request for client ID {client_id} successfull. [204]")
    return ''
        
