FROM python:3.8

WORKDIR /app

RUN mkdir src
COPY ./__init__.py ./src

RUN mkdir -p src/rest_api
COPY ./rest_api ./src/rest_api

RUN mkdir -p src/training
COPY ./training ./src/training

RUN pip install -r ./src/rest_api/requirements.txt
RUN pip install -r ./src/training/requirements.txt

ENTRYPOINT FLASK_APP=/app/src/rest_api/main.py flask run --host=0.0.0.0

EXPOSE 5000
