all: prety lint
lint:
	poetry run flake8 . --ignore E501,W503
prety:
	poetry run isort .
	poetry run black .
serv:
	docker compose up -d --build
test: prety lint
	BAKENEKO_TARGET=dev docker compose up -d --build
	docker wait bakeneko-web
	rm -rf ./reports/*
	docker cp bakeneko-web:/code/htmlcov ./reports/cov
	docker cp bakeneko-web:/code/report.html ./reports/report.html
	docker compose down -v