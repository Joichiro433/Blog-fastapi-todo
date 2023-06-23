#/bin/bash

cd app/
# alembic init migrations
alembic revision --autogenerate -m "init"
alembic upgrade head