FROM python:3.11
RUN pip install poetry
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry install --without dev
COPY /src /src
WORKDIR .