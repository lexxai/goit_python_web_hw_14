@echo off
PUSHD ..\hw14

alembic init migrations

alembic revision --autogenerate -m "Init"

POPD