from fastapi import APIRouter, HTTPException
from infra.sql.database.database import clients
from infra.schemas.clients.clients_schema import Client
from typing import List

clients_router = APIRouter()

@clients_router.post("/", response_model=Client, status_code=201)
async def create_task(client: Client):
    clients.append(client)
    return client
    

@clients_router.get("/", response_model=List[Client], status_code=200)
async def read_tasks():
    return clients

@clients_router.get("/{client_id}", response_model=Client, status_code=200)
async def read_task(client_id: int):
    for client in clients:
        if client.id == client_id:
            return client
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")
            
@clients_router.put("/{client_id}", response_model=Client, status_code=200)
async def update_task(client_id: int, task_updated: Client):
    for client in clients:
        if client.id == client_id:
            for key, value in task_updated:
                setattr(client, key, value)
            return client
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")        
            
@clients_router.delete("/{client_id}", status_code=204)
async def delete_task(client_id: int):
    for client in clients:
        if client.id == client_id:
            clients.remove(client)
            return ''
        raise HTTPException(status_code=404, detail="The following client doesn't exist!")  
