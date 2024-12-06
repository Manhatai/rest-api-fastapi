from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.clients.clients_schema import ClientSchema
from infra.sql.clients.clients_model import ClientsTable

clients_router = APIRouter()

@clients_router.get("/clients", response_model=list[ClientSchema], status_code=200)
async def get_clients(db: Session = Depends(get_db)):
    all_clients = db.query(ClientsTable).all()
    return all_clients

@clients_router.get("/clients/{client_id}", response_model=ClientSchema, status_code=200)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    specific_client = db.query(ClientsTable).filter(ClientsTable.id == client_id).first()
    if not specific_client:
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")
    return specific_client

@clients_router.post("/clients", response_model=ClientSchema, status_code=201)
async def create_client(client: ClientSchema, db: Session = Depends(get_db)):
    new_client = ClientsTable( # constructor
        firstName = client.firstName,
        phone = client.phone
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@clients_router.put("/clients/{client_id}", response_model=ClientSchema, status_code=200)
async def update_client(client_id: int, update_data: ClientSchema, db: Session = Depends(get_db)):
    client = db.query(ClientsTable).filter(ClientsTable.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="The following client doesn't exist!") 
    for key, value in update_data.model_dump(exclude_unset=True).items(): # .items() for value pairs
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client      
            
@clients_router.delete("/clients/{client_id}", status_code=204)
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    deleted_client = db.query(ClientsTable).filter(ClientsTable.id == client_id).first()
    if not deleted_client:
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")  
    db.delete(deleted_client)
    db.commit()
    return ''
        
