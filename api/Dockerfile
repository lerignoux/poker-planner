FROM python:3.9-alpine

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

cmd ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
