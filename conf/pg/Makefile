
# The name of the remote file
PG_NAME = biostardb-daily-2024-06-04.gz
PG_FILE = sql/${PG_NAME}
PG_URL = www@test.biostars.org:/home/www/data/biostars/${PG_NAME}

DB = test_database
USER = test_user
PASSWD = test_passwd

usage:
	@echo "Use the source, Luke!"

${PG_FILE}:
	mkdir -p $(dir ${PG_FILE})
	rsync -avzL --progress ${PG_URL} ${PG_FILE}

get: ${PG_FILE}
	ls -l ${PG_FILE}

reset:
	psql -c "DROP DATABASE IF EXISTS ${DB};"
	psql -c "CREATE DATABASE ${DB};"
	psql -c "DROP USER IF EXISTS ${USER};"
	psql -c "CREATE USER ${USER} WITH PASSWORD '${PASSWD}';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB} TO ${USER};"

load: ${PG_FILE}
	gunzip -c ${PG_FILE} | psql -U ${USER} -d ${DB}


