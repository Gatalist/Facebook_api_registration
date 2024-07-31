# pull official base image
FROM python:3.12

# create the app user
RUN addgroup --system app && adduser --system --group app

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y curl gcc \
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libxkbcommon0 libasound2

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/poetry python3 -

ENV PATH="${PATH}:/root/poetry/bin"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/app

# copy project
COPY pyproject.toml /home/app

# install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN playwright install

# copy project
COPY . .
