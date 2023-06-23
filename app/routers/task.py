from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

import cruds.task as task_crud
from models.task import Task, TaskRead, TaskCreate, TaskUpdate
from db import get_session


router = APIRouter(
    prefix='/tasks',
    tags=['Task'],
    responses={404: {'message': 'Not found'}})


@router.get('/', response_model=list[TaskRead])
def read_tasks(
        *, 
        session: Session = Depends(get_session), 
        done: bool | None = Query(None)
    ) -> list[TaskRead]:
    """
    Read tasks from the database, filtered by the 'done' flag.

    Parameters
    ----------
    done : bool | None, optional, **[query parameter]**\n
        The value of the 'done' flag to filter tasks by, by default None.

    Returns
    -------
    list[TaskRead]\n
        The list of tasks.
    """
    return task_crud.read_tasks(session=session, done=done)


@router.get('/{task_id}', response_model=TaskRead)
def read_task(
        *, 
        session: Session = Depends(get_session), 
        task_id: int
    ) -> TaskRead:
    """
    Read a task from the database by its ID.

    Parameters
    ----------
    task_id : int, **[path parameter]**\n
        The ID of the task to read.

    Returns
    -------
    TaskRead\n
        The requested task if found, otherwise raises a 404 HTTPException.
    """

    task: Task | None = task_crud.read_task(session=session, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


@router.post('/', response_model=TaskCreate)
def create_task(
        *, 
        session: Session = Depends(get_session), 
        task: TaskCreate
    ) -> TaskCreate:
    """
    Create a new task in the database.

    Parameters
    ----------
    task : TaskCreate, **[body parameter]**\n
        The task creation object.

    Returns
    -------
    TaskCreate\n
        The created task.
    """
    created_task = task_crud.create_task(session=session, task=task)
    return created_task


@router.patch('/{task_id}', response_model=TaskRead)
def update_task(
        *, 
        session: Session = Depends(get_session), 
        task_id: int, 
        task: TaskUpdate
    ) -> TaskRead:
    """
    Update a task in the database.

    Parameters
    ----------
    task_id : int, **[path parameter]**\n
        The ID of the task to update.
    task : TaskUpdate, **[body parameter]**\n
        The update object containing the new task data.

    Returns
    -------
    TaskRead\n
        The updated task.
    """
    org_task: Task | None = task_crud.read_task(session=session, task_id=task_id)
    if org_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task_crud.update_task(session=session, db_task=org_task, task=task)


@router.delete('/{task_id}')
def delete_task(
        *, 
        session: Session = Depends(get_session), 
        task_id: int
    ) -> dict[str, bool]:
    """
    Delete a task from the database.

    Parameters
    ----------
    task_id : int, **[path parameter]**\n
        The ID of the task to delete.

    Returns
    -------
    dict[str, bool]\n
        A dictionary with a single key 'ok' and a value of True, indicating successful deletion.
    """
    task_to_delete: Task | None = task_crud.read_task(session=session, task_id=task_id)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail='Task not found')
    task_crud.delete_task(session=session, db_task=task_to_delete)
    return {'ok': True}
