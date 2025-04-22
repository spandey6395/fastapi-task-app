from sqlalchemy.orm import Session
from .models import Task, TaskStatus
from .schemas import TaskCreate, TaskUpdate
from uuid import UUID


def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: UUID):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: UUID, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: UUID):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task
