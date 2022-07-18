all: prety lint test
lint:
	poetry run flake8 . --ignore E501,W503
prety:
	poetry run isort .
	poetry run black .
serv:
	docker compose up -d --build
test-start:
	BAKENEKO_TARGET=dev docker compose up -d --build
	docker wait bakeneko-web
test-report:
	rm -rf ./reports/*
	docker cp bakeneko-web:/code/htmlcov ./reports/cov
	docker cp bakeneko-web:/code/report.html ./reports/report.html
test-end:
	docker compose down -v
test: test-start test-report test-end