import socket
import ssl

BUFFER_SIZE = 1024


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
            print("Answer from DNS Server: ")
            print(data.decode("ISO-8859-1", "ignore"))
            return data

        except Exception as e:
            print(e)
        finally:
            tls_wrapper.close()

    def handler(self, data, address, socket, dns_addr, ca_path):
        answer = self.send_query(dns_addr, data, ca_path)
        if answer:
            try:
                print("Proxy Ok: %s", answer.decode("ISO-8859-1", "ignore"))
                socket.sendto(answer[2:], address)
            except Exception as e:
                print(e)
        else:
            print(e)
