import socket
import ssl
import logging

BUFFER_SIZE = 1024
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class TCP:
    def send_query(self, dns, query, ca_path):
        """Send request to a secure DNS Server from TCP Socket"""
        try:
            # tcp socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(100)

            # tls context to wrap the socket connection
            ctx = ssl.create_default_context()
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ctx.verify_mode = ssl.CERT_REQUIRED
            ctx.check_hostname = True
            ctx.load_verify_locations(ca_path)

            tls_wrapper = ctx.wrap_socket(sock, server_hostname=dns)
            tls_wrapper.connect((dns, 853))

            logging.info("tcp client request (first 10 bits): %s", query[:10])
            tls_wrapper.sendall(query)

            data = tls_wrapper.recv(BUFFER_SIZE)
            logging.info("answer from DNS/TCP (first 10 bits): %s", data[:10])
            # logging.info(data.decode("ISO-8859-1", "ignore"))
            return data

        except Exception as e:
            logging.error("initiating tcp error: %s",str(e))
        finally:
            tls_wrapper.close()

    def handler(self, data, address, conn, dns_addr, ca_path):
        answer = self.send_query(dns_addr, data, ca_path)
        if answer:
            try:
                logging.info("tcp proxy done!")
                conn.send(answer)
            except Exception as e:
                logging.error("initializing tcp handler: ", e)
        else:
            logging.error("no response from tcp handler")
