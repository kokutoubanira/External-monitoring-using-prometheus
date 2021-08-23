FROM python:3.6.14-alpine

WORKDIR /app

COPY ./app.py ./app.py

RUN pip install Flask

CMD ["python", "app.py"]