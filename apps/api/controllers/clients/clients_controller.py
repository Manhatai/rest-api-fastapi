from fastapi import APIRouter, HTTPException, Depends
from infra.sql.database.database import get_db
from sqlalchemy.orm import Session
from infra.schemas.clients.clients_schema import Client
from infra.sql.clients.clients_model import ClientsTable
from typing import List

clients_router = APIRouter()

@clients_router.post("/clients", response_model=Client, status_code=201)
async def create_task(client: Client, db: Session = Depends(get_db)):
    clients.append(client)
    return client
    

@clients_router.get("/clients", response_model=List[Client], status_code=200)
async def read_tasks(db: Session = Depends(get_db)):
    all_clients = db.query(Client).all()
    return all_clients

@clients_router.get("/clients/{client_id}", response_model=Client, status_code=200)
async def read_task(client_id: int):
    for client in clients:
        if client.id == client_id:
            return client
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")
            
@clients_router.put("/clients/{client_id}", response_model=Client, status_code=200)
async def update_task(client_id: int, task_updated: Client):
    for client in clients:
        if client.id == client_id:
            for key, value in task_updated:
                setattr(client, key, value)
            return client
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")        
            
@clients_router.delete("/clients/{client_id}", status_code=204)
async def delete_task(client_id: int):
    for client in clients:
        if client.id == client_id:
            clients.remove(client)
            return ''
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")  
