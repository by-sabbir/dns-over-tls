import logging
import socket
from threading import Thread

from handlers.tcp import TCP
from handlers.udp import UDP

PORT = 53
DNS = "1.1.1.1"
ADDRESS = "0.0.0.0"
CA_CERT = "/etc/ssl/cert.pem"
BUFFER_SIZE = 4096

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


class DoTProxy:
    @staticmethod
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
                logging.info(
                    "dns query from client: %s", data
                )  # for string data.decode("ISO-8859-1", "replace")
                tcp.handler(data, address=addr, conn=conn, dns_addr=dns, ca_path=ca)
        except Exception as e:
            logging.error("listening tcp port error: %s", e)
        finally:
            sock.close()

    @staticmethod
    def listen_udp(address=ADDRESS, port=PORT, dns=DNS, ca=CA_CERT):
        """Listening for DNS UDP requests"""
        logging.info("udp server started at port: %s", PORT)
        try:
            udp = UDP()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((address, port))
            while True:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                logging.info(
                    "udp query: %s", data
                )  # for string .decode("ISO-8859-1", "replace")
                udp.handler(data, address=addr, socket=sock, dns=dns, cert=ca)
        except Exception as e:
            logging.error("listening udp port error: %s", e)
        finally:
            sock.close()

    def serve(self):
        args = (ADDRESS, PORT, DNS, CA_CERT)

        threads = []
        threads.append(Thread(target=self.listen_tcp, args=args))
        threads.append(Thread(target=self.listen_udp, args=args))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    proxy = DoTProxy()
    proxy.serve()
