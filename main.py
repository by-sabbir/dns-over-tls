import socket
from handler.tcp import TCP
from handler.udp import UDP
from multiprocessing import Process
import logging

PORT = 53
DNS = "1.1.1.1"
ADDRESS = "0.0.0.0"
CA_CERT = "/etc/ssl/cert.pem"
BUFFER_SIZE = 1024

processes = []
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def listen_tcp(address=ADDRESS, port=PORT, dns=DNS, ca=CA_CERT):
    """Listening for DNS TCP requests"""
    logging.info("tcp server started at port: %s", PORT)
    try:
        tcp = TCP()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address, port))
        # accept upto 5 connections
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            data = conn.recv(BUFFER_SIZE)
            logging.info("dns query from client: %s", data) # for string data.decode("ISO-8859-1", "replace")
            tcp.handler(data, address=addr, conn=conn, dns_addr=dns, ca_path=ca)
    except Exception as e:
        logging.error("listening tcp port error: %s", e)
    finally:
        sock.close()

def listen_udp(address=ADDRESS, port=PORT, dns=DNS, ca=CA_CERT):
    """Listening for DNS UDP requests"""
    logging.info("udp server started at port: %s", PORT)
    try:
        udp = UDP()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            logging.info("udp query: %s", data) # for string .decode("ISO-8859-1", "replace")
            udp.handler(data, address=addr, socket=sock, dns=dns, cert=ca)
    except Exception as e:
        logging.error("listening udp port error: %s", e)
    finally:
        sock.close()


if __name__ == "__main__":
    args = (ADDRESS, PORT, DNS, CA_CERT)

    processes.append(Process(target=listen_tcp, args=args))
    processes.append(Process(target=listen_udp, args=args))

    for process in processes:
        process.start()

    for process in processes:
        process.join()
