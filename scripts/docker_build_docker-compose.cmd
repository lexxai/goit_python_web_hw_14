@echo off
PUSHD ..

docker-compose --env-file .env-prod up -d code --build
timeout 1
docker attach web_hw13-code-1

docker-compose down 

POPD