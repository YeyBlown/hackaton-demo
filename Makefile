postgres.create:
	 docker create --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -p 5432:5432 -v /data\:/var/lib/postgresql/data postgres

postgres.run:
	docker start postgresql

postgres.stop:
	docker stop postgresql

fmt:
	black ./pkg --check

fmt.fix:
	black ./pkg

lint:
	pylint ./pkg --rcfile .pylintrc

dockr:
	# backend
	docker rm -f demo-server || true
	docker build . -f docker/.Dockerfile --tag demo-server
	docker create --name demo-server demo-server
	# frontend
	make -C client/ dockr

run:
	make -C docker/ run

stop:
	make -C docker/ stop

db.upgrade:
	# TODO: add to server script(docker image) or create separate
	psql -c 'create database maindb;' postgresql://myusername:mypassword@localhost:5432 || true
	alembic upgrade head
