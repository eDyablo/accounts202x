ARG BASE_IMAGE=alpine

FROM ${BASE_IMAGE} AS build

LABEL org.opencontainers.image.authors="eyablonsky@gmail.com"

RUN apk update --no-cache \
  && apk add \
  build-base \
  postgresql-dev \
  py3-pip \
  python3-dev

WORKDIR /opt/accounts

COPY requirements.txt .

RUN python3 -m venv venv \
  && source venv/bin/activate \
  && python -m pip install --upgrade pip --no-cache-dir \
  && python -m pip install --requirement requirements.txt --no-cache-dir \
  && python -m pip freeze > requirements.txt

FROM ${BASE_IMAGE} AS package

LABEL org.opencontainers.image.authors="eyablonsky@gmail.com"

RUN apk update --no-cache \
  && apk add \
  libpq \
  python3

WORKDIR /opt/accounts

COPY --from=build /opt/accounts .

COPY *.py .

ENV FLASK_ENV=development

CMD [ "sh", "-c", "venv/bin/flask run --host=0.0.0.0 ${PORT:+--port=${PORT}}" ]
