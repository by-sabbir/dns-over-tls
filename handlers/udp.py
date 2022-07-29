import logging
import socket
import ssl
import traceback


BUFFER_SIZE = 4096
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class UDP:
    def send_query(self, dns, query, ca_path):
        """Send request to a secure DNS Server from UDP Socket"""
        try:
            server = (dns, 853)

            # tcp socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(100)

            ctx = ssl.create_default_context()
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ctx.verify_mode = ssl.CERT_REQUIRED
            ctx.check_hostname = True
            ctx.load_verify_locations(ca_path)

            tls_wrapper = ctx.wrap_socket(sock, server_hostname=dns)
            tls_wrapper.connect(server)

            udp_len = bytes([00]) + bytes([len(query)])
            tcp_data = udp_len + query
            tls_wrapper.send(tcp_data)
            data = tls_wrapper.recv(BUFFER_SIZE)
            logging.info("udp client request (first 10 bits): %s", tcp_data[:10])
            logging.info("answer from DNS/UDP (first 10 bits): %s", data[:10])

            return data

        except Exception as e:
            traceback.format_exc()
            logging.error("initializing udp: %s", e)
        finally:
            tls_wrapper.close()

    def handler(self, data, address, socket, dns, cert):
        answer = self.send_query(dns, data, cert)
        if answer:
            try:
                logging.info("udp proxy done!")
                socket.sendto(answer[2:], address)
            except Exception as e:
                logging.error("initializing handler: %s", e)
        else:
            logging.error("no response from udp handler")
