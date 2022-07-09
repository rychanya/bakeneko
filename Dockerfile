FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10 as prod
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./bakeneko /code/bakeneko
CMD ["uvicorn", "bakeneko.web:app", "--host", "0.0.0.0"]

FROM python:3.10 as requirements-dev-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --dev

FROM python:3.10 as dev
WORKDIR /code
COPY --from=requirements-dev-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./bakeneko /code/bakeneko
COPY ./tests /code/tests
CMD ["pytest", "--cov-report", "html", "--cov=bakeneko", "tests/", "--html=report.html", "--self-contained-html"]
