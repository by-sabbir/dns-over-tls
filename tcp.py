import socket
import ssl

BUFFER_SIZE = 1024

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

            print("client request: ", query.decode("ISO-8859-1", "ignore"))
            tls_wrapper.sendall(query)

            data = tls_wrapper.recv(BUFFER_SIZE)
            print("Answer from DNS: ")
            print(data.decode("ISO-8859-1", "ignore"))
            return data

        except Exception as e:
            print(str(e))
        finally:
            tls_wrapper.close()

    def handler(self, data, address, conn, dns_addr, ca_path):
        answer = self.send_query(dns_addr, data, ca_path)
        if answer:
            try:
                print(
                    "proxy ok: ",
                )
                conn.send(answer)
            except Exception as e:
                print(e)
        else:
            print("no response")