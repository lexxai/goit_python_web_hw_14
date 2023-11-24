PUSHD ..\hw14

taskkill /IM "uvicorn.exe" /F
uvicorn main:app --reload --port 9000
taskkill /IM "uvicorn.exe" /F

POPD