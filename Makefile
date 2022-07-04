all: prety lint
lint:
	poetry run flake8 . --ignore E501,W503
prety:
	poetry run isort .
	poetry run black .
serv:
	docker compose -f "docker-compose.yml" up -d --build
clean:
	docker volume rm bakeneko_postgres_data
test: prety lint
	docker compose -f "docker-compose-dev.yml" up -d --build
	docker wait bakeneko-test
	docker compose -f "docker-compose-dev.yml" down