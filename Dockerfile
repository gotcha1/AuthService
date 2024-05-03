###########################################################################
# Build dev base image
###########################################################################
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS dev-base

# set working directory
WORKDIR /var

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MAX_WORKERS=1
ENV LOG_LEVEL=debug
ENV PORT 8080

RUN apt update \
    && apt-get install -y git git-lfs
RUN git config --global core.autocrlf true \
    && git config --global core.ignorecase true \
    && git config --global core.filemode false

# install system dependencies
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  curl \
  colorized-logs \
  daemontools \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip


COPY ./src/app /app
WORKDIR /app


RUN pip3 install --upgrade pip


# Install Poetry (append poetry bin path)
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python - && \
  poetry config virtualenvs.create false


# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

###########################################################################
# Build dev env image
###########################################################################
FROM dev-base AS dev-env
RUN poetry install --no-root
COPY ./src /app

###########################################################################
# Build lint image
###########################################################################
FROM dev-env AS dev-linter
COPY ./setup.cfg /app
RUN pylama -o setup.cfg src

###########################################################################
# Build utest coverage image
###########################################################################
FROM dev-env AS dev-coverage
COPY ./src /var
WORKDIR /var
RUN coverage run -m pytest -p no:warnings --junitxml=junit.xml --cov=app --cov-report html --cov-report xml

###########################################################################
# Build runtime image
###########################################################################
FROM dev-base

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
