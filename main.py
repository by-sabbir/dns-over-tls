import socket
from tcp import Tcp


PORT = 53
DNS = "8.8.8.8"
ADDRESS = "0.0.0.0"
CA_CERT = "/etc/ssl/cert.pem"


def listen_tcp(address=ADDRESS, port=PORT, dns=DNS, ca=CA_CERT):
    """Listening for DNS TCP requests"""
    try:
        tcp = Tcp()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address, port))
        sock.listen(2)
        while True:
            conn, addr = sock.accept()
            print("Conecttion info: ", conn)
            data = conn.recv(4096)
            print(data.decode("ISO-8859-1", "replace"))
            print(addr, conn)
            tcp.handler(data, address=addr, conn=conn, dns_addr=dns, ca_path=ca)
    except Exception as e:
        print(e)
    finally:
        sock.close()


if __name__ == "__main__":
    listen_tcp(ADDRESS, PORT, DNS, CA_CERT)
