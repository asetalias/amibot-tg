FROM python:3.8-slim-buster

ENV MONGO_URI "Value 1"
ENV MONGO_DATABASE "Value 2"

WORKDIR /app

# Copy the poetry files to the container
COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

# Install the dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

CMD ["poetry", "run", "python", "main.py"]
