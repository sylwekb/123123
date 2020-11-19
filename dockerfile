FROM python:3.8.6-slim-buster

COPY . .

RUN pip install -r requirements.txt
RUN pip install requests[socks]

RUN mkdir /code
WORKDIR /code