from sqlmodel import select, Session

from models.task import Task, TaskCreate, TaskUpdate


def create_task(session: Session, task: TaskCreate) -> Task:
    """
    Create a new task in the database.

    Parameters
    ----------
    session : Session
        The database session.
    task : TaskCreate
        The task creation object.

    Returns
    -------
    Task
        The created task.
    """
    db_task: Task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def read_task(session: Session, task_id: int) -> Task | None:
    """
    Read a task from the database by its ID.

    Parameters
    ----------
    session : Session
        The database session.
    task_id : int
        The ID of the task to read.

    Returns
    -------
    Task | None
        The requested task if found, otherwise None.
    """
    task: Task | None = session.get(Task, task_id)
    return task


def read_tasks(session: Session, done: bool | None = None) -> list[Task]:
    """
    Read tasks from the database, filtered by the 'done' flag.

    Parameters
    ----------
    session : Session
        The database session.
    done : bool | None, optional
        The value of the 'done' flag to filter tasks by, by default None.

    Returns
    -------
    list[Task]
        The list of tasks.
    """
    query = select(Task)
    if done is not None:
        query = query.where(Task.done == done)
    tasks: list[Task] = session.exec(query).all()
    return tasks


def update_task(session: Session, db_task: Task, task: TaskUpdate) -> Task:
    """
    Update a task in the database.

    Parameters
    ----------
    session : Session
        The database session.
    db_task : Task
        The task object to update.
    task : TaskUpdate
        The update object containing the new task data.

    Returns
    -------
    Task
        The updated task.
    """
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, db_task: Task) -> None:
    """
    Delete a task from the database.

    Parameters
    ----------
    session : Session
        The database session.
    db_task : Task
        The task object to delete.

    Returns
    -------
    None
    """
    session.delete(db_task)
    session.commit()
    return
