dockr:
	docker rm -f demo-client || true
	docker build . -f docker/.Dockerfile --tag demo-client
	docker create --name demo-client demo-client