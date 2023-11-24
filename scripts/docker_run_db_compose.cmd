@echo off

PUSHD ..
docker compose  --env-file .env-prod --file docker-compose-db.yml  up -d 
rem change password
docker exec -it web_hw14-pg-1 bash -c "echo waiting until DB is up for 2 sec;sleep 2;psql -U ${POSTGRES_USERNAME} -d ${POSTGRES_DB} -c \"ALTER USER ${POSTGRES_USERNAME} WITH PASSWORD '${POSTGRES_PASSWORD}'\""   
POPD

sql_upgrade.cmd

   

