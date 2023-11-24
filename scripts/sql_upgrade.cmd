@echo off
PUSHD ..\hw14

rem alembic revision --autogenerate -m "Updates"
alembic upgrade head 

POPD