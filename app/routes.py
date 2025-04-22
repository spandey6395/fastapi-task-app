from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from .database import get_db, logger  # Import logger
from .schemas import TaskCreate, TaskResponse, TaskUpdate
from .crud import create_task, get_tasks, update_task, delete_task
from sqlalchemy.sql import text

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: UUID, task: TaskUpdate, db: Session = Depends(get_db)
):
    updated_task = update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: UUID, db: Session = Depends(get_db)):
    deleted_task = delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        with db.begin():  # Ensure transaction context
            db.execute(text("SELECT 1"))
        return {"status": "Database connection OK"}
    except Exception as e:
        logger.error(f"Health check failed: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=503, detail="Database connection failed")
