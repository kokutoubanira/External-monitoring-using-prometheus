FROM python:3.9.7-buster

WORKDIR /app

COPY ./webhook_reciver.py ./webhook_reciver.py
COPY ./requirement.txt  ./requirement.txt

RUN pip install --upgrade pip
RUN pip install -r requirement.txt

CMD ["python", "webhook_reciver.py"]