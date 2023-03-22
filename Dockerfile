FROM python:3.8-slim-buster

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY *.py ./

RUN mkdir data

ENTRYPOINT pipenv run python3 bot.py