from collections.abc import Generator

from sqlmodel import create_engine, Session

import settings


engine = create_engine(settings.DB_URI, echo=True)

def get_session() -> Generator[Session, None, None]:
    """Returns a generator that can be used as a context manager to generate database sessions.

    Yields
    ------
    session : sqlmodel.Session
        The database session object.
    """
    with Session(engine) as session:
        yield session
