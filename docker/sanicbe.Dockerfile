# syntax=docker/dockerfile:1
ARG APP_ENV

# FROM python:slim as base
FROM python:3.10-slim as base
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install gcc -y \
    && apt-get clean

FROM base as dev-preinstall
COPY ./sanicbe/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/sanic \
    pip install -r requirements.txt

FROM base as test-preinstall
COPY ./sanicbe/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/sanic \
    pip install -r requirements.txt

FROM base as prod-preinstall
COPY ./sanicbe/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/sanic \
    pip install --user -r requirements.txt


FROM ${APP_ENV}-preinstall as postinstall


FROM postinstall as development
WORKDIR /app

VOLUME [ "/app" ]
CMD ["python", "src/main.py"]


FROM postinstall as testing
WORKDIR /app

VOLUME [ "/app" ]
CMD ["pytest", "--verbose", "src/tests"]


# FROM python:slim as production
FROM python:3.10-slim as production
WORKDIR /app
COPY --from=postinstall /root/.local /root/.local
COPY ./sanicbe/src .

ENV PATH=/root/.local/bin:$PATH

VOLUME [ "/app" ]
CMD ["python", "main.py"]