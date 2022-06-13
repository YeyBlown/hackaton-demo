hello:
	echo "hello world"

create-postgres:
	 docker create --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -p 5432:5432 -v /data\:/var/lib/postgresql/data postgres

run-postgres:
	docker start postgresql

stop-postgres:
	docker stop postgresql

format:
	black ./pkg