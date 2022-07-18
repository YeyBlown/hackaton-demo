dockr:
	docker rm -f demo-server || true
	docker build . -f docker/.Dockerfile --tag demo-server
	docker create --name demo-server demo-server

fmt:
	black ./pkg --check

fmt.fix:
	black ./pkg

lint:
	pylint ./pkg --rcfile .pylintrc