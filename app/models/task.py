from typing import Optional

from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    title: str = Field(description='task name', nullable=False)
    done: bool = Field(default=False, description='done flag', nullable=False)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: str
    done: bool
