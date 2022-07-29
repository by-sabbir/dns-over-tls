.PHONY: build run test-udp test-tcp multiple-client

SERVICE_NAME=dns-over-tcp
SERVICE_PORT=53

build:
	docker build -t $(SERVICE_NAME) .

run:
	docker run -itd --name $(SERVICE_NAME) -p $(SERVICE_PORT):53/tcp -p $(SERVICE_PORT):53/udp $(SERVICE_NAME)

logs:
	docker logs -f $(SERVICE_NAME)

test-udp:
	dig @0.0.0.0 -p $(SERVICE_PORT) sabbir.dev

test-tcp:
	dig @0.0.0.0 -p $(SERVICE_PORT) sabbir.dev +tcp

multiple-client:
	dig @0.0.0.0 -p $(SERVICE_PORT) sabbir.dev +tcp
	dig @0.0.0.0 -p $(SERVICE_PORT) sabbir.dev udp
	dig @0.0.0.0 -p $(SERVICE_PORT) google.com +tcp
	dig @0.0.0.0 -p $(SERVICE_PORT) google.com
	dig @0.0.0.0 -p $(SERVICE_PORT) yahoo.com +tcp
	dig @0.0.0.0 -p $(SERVICE_PORT) yahoo.com
	dig @0.0.0.0 -p $(SERVICE_PORT) udemy.com +tcp
	dig @0.0.0.0 -p $(SERVICE_PORT) udemy.com
	dig @0.0.0.0 -p $(SERVICE_PORT) coursera.com +tcp
	dig @0.0.0.0 -p $(SERVICE_PORT) coursera.com

