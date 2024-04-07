FROM python:3.12-alpine as requirements-stage

WORKDIR /tmp

RUN pip install poetry --no-cache-dir

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with prod

FROM python:3.12-alpine

WORKDIR /usr/scr/eduapi

COPY --from=requirements-stage /tmp/requirements.txt /usr/scr/eduapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/scr/eduapi/requirements.txt

COPY ./alembic.ini /usr/scr/eduapi/alembic.ini
COPY ./migrations /usr/scr/eduapi/migrations
COPY ./api /usr/scr/eduapi/api

CMD [ \
    "gunicorn", "api:get_app()", \
    "--workers", "2", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:80" \
]