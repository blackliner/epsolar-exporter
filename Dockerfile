FROM python:3.11.0-slim-buster@sha256:36457c7a4d25734dd93c768aadcaed6073403a222ff52542d69ba2ea926df22b

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.14 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    curl \
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY . /src

WORKDIR /src

RUN poetry install --no-interaction --no-ansi

CMD [ "epsolar-exporter" ]
