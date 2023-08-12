FROM python:3.11-slim-buster

WORKDIR /app

# Copy the poetry files to the container
COPY pyproject.toml poetry.lock app.env /app/

RUN pip install poetry

# Install the dependencies
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . /app

EXPOSE 2205

CMD ["poetry", "run", "python", "main.py"]
