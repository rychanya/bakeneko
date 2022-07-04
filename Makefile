all: prety lint test
lint:
	poetry run flake8 . --ignore E501,W503
prety:
	poetry run isort .
	poetry run black .
test:
	poetry run pytest --cov-report html --cov=bakeneko tests/ --html=report.html --self-contained-html
serv:
	docker compose -f "docker-compose.yml" up -d --build
clean:
	docker volume rm bakeneko_postgres_data