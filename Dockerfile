# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

COPY ./src ./src
# Copy the pyproject.toml and poetry.lock (if present)
COPY pyproject.toml poetry.lock* .

# Install the dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Start with a shell that keeps the container alive
CMD ["tail", "-f", "/dev/null"]
