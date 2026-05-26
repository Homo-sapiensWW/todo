from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


tasks_db = []
counter = 0

@app.get('/tasks')
def get_tasks():
    return tasks_db

@app.post('/tasks')
def add_tasks(task: Task):
    global counter
    counter += 1
    task.id = counter
    tasks_db.append(task)
    return {'message': 'task added successfully', 'id': counter}

@app.get('/tasks/{task_id}')
def get_task(task_id: int):
    for i in range(len(tasks_db)):
        if tasks_db[i].id == task_id:
            return tasks_db[i]
    return 'Have no task with this id'

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    for i in tasks_db:
        if i.id == task_id:
            tasks_db.pop(i)

@app.patch('/tasks/{task_id}')
def update_task(task: TaskUpdate, task_id: int):
    for i in range(len(tasks_db)):
        if tasks_db[i].id == task_id:
            info_dict = task.model_dump(exclude_unset=True)
            for j in info_dict:
                setattr(tasks_db[i], j, info_dict[j])
            return tasks_db[i]