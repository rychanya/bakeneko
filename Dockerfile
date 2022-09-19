FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM node as vue-build
WORKDIR /tmp
COPY ./web-vue/package*.json /tmp/
RUN npm install
COPY ./web-vue /tmp
RUN npm run build

FROM python:3.10
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./bakeneko /code/bakeneko
COPY --from=vue-build /tmp/dist /code/web-vue/dist
CMD ["uvicorn", "bakeneko.web:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80
