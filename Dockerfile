FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv lock

RUN pipenv install --deploy --ignore-pipfile

COPY . /app/

EXPOSE 5000

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
