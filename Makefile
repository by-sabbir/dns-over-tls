.PHONY: build run test-udp test-tcp multiple-client cleanup

SERVICE_NAME=dns-over-tcp
SERVICE_PORT=853
SERVICE_IP=0.0.0.0
build:
	docker build -t $(SERVICE_NAME) .

run:
	docker run -itd --name $(SERVICE_NAME) -p $(SERVICE_PORT):53/tcp -p $(SERVICE_PORT):53/udp $(SERVICE_NAME)

logs:
	docker logs -f $(SERVICE_NAME)

test-udp:
	dig sabbir.dev @0.0.0.0 -p $(SERVICE_PORT) 

test-tcp:
	dig sabbir.dev +tcp @0.0.0.0 -p $(SERVICE_PORT) 

multiple-client:
	dig sabbir.dev +tcp @0.0.0.0 -p $(SERVICE_PORT) 
	dig sabbir.dev udp @0.0.0.0 -p $(SERVICE_PORT) 
	dig google.com +tcp @0.0.0.0 -p $(SERVICE_PORT) 
	dig google.com @0.0.0.0 -p $(SERVICE_PORT) 
	dig yahoo.com +tcp @0.0.0.0 -p $(SERVICE_PORT) 
	dig yahoo.com @0.0.0.0 -p $(SERVICE_PORT) 
	dig udemy.com +tcp @0.0.0.0 -p $(SERVICE_PORT) 
	dig udemy.com @0.0.0.0 -p $(SERVICE_PORT) 
	dig coursera.com +tcp @0.0.0.0 -p $(SERVICE_PORT) 
	dig coursera.com @0.0.0.0 -p $(SERVICE_PORT) 

cleanup:
	docker rm -f $(SERVICE_NAME)
