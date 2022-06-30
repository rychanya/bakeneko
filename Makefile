all: prety lint test
lint:
	poetry run flake8 . --ignore E501,W503
prety:
	poetry run isort .
	poetry run black .
test:
	poetry run pytest --cov-report html --cov=bakeneko tests/
serv:
	poetry run python bakeneko/dev_server.py