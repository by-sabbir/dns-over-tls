FROM python:3.10-slim-bullseye

RUN apt-get update
RUN apt-get install -y --no-install-recommends

COPY ./cert.pem /etc/ssl/cert.pem
WORKDIR /app

COPY . .

EXPOSE 53/tcp 53/udp


CMD [ "python", "daemon.py" ]
