all: prety lint pytest
lint:
	poetry run flake8 . --ignore E501,W503
prety:
	poetry run isort .
	poetry run black .
serv:
	docker compose up --build
pytest:
	poetry run pytest --cov-report html --cov=bakeneko tests/ --html=report.html --self-contained-html
serv-loc:
	poetry run uvicorn bakeneko.web:app --reload
db:
	docker run --name test-db -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=db -d postgres