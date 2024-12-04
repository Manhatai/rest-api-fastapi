from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

tasks = []

@app.post("/tasks/", response_model=Task, status_code=201)
async def create_task(task: Task):
    tasks.append(task)
    return task
    

@app.get("/tasks/", response_model=List[Task], status_code=200)
async def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task, status_code=200)
async def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
        raise HTTPException(status_code=404, detail="The following task doesn't exist!")
            
@app.put("/tasks/{task_id}", response_model=Task, status_code=200)
async def update_task(task_id: int, task_updated: Task):
    for task in tasks:
        if task.id == task_id:
            for key, value in task_updated:
                setattr(task, key, value)
            return task
        raise HTTPException(status_code=404, detail="The following task doesn't exist!")        
            
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return ''
        raise HTTPException(status_code=404, detail="The following task doesn't exist!")  


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080) # or localhost