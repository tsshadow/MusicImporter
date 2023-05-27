# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

#install dependencies
RUN apt update && apt install wget -y

RUN wget http://ftp.nl.debian.org/debian/pool/non-free/u/unrar-nonfree/unrar_5.>
    dpkg -i *.deb && \
    apt update && \
    apt install unzip p7zip-full -y

WORKDIR /app

COPY . .
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD ["python3" , "main.py", "docker"]
