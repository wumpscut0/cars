FROM python:3.12.4-alpine

WORKDIR /app

ENV POETRY_VERSION=1.8.3
ENV PYTHONONBUFFERED=0

RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir poetry==$POETRY_VERSION

RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-root --no-ansi

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]