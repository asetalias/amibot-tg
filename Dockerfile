FROM python:3.11-slim-buster

ENV MONGO_URI "mongo url"
ENV MONGO_DATABASE "users"
ENV TOKEN "TOKEN"

WORKDIR /app

# Copy the poetry files to the container
COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

# Install the dependencies
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . /app

CMD ["poetry", "run", "python", "main.py"]
