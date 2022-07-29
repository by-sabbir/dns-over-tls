import socket
from tcp import TCP
from udp import UDP


PORT = 53
DNS = "1.1.1.1"
ADDRESS = "0.0.0.0"
CA_CERT = "/etc/ssl/cert.pem"
BUFFER_SIZE = 1024

def listen_tcp(address=ADDRESS, port=PORT, dns=DNS, ca=CA_CERT):
    """Listening for DNS TCP requests"""
    print("tcp listener")
    try:
        tcp = TCP()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address, port))
        # accept upto 5 connections
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            print("Conecttion info: ", conn)
            data = conn.recv(BUFFER_SIZE)
            print(data.decode("ISO-8859-1", "replace"))
            print(addr, conn)
            tcp.handler(data, address=addr, conn=conn, dns_addr=dns, ca_path=ca)
    except Exception as e:
        print(e)
    finally:
        sock.close()

def listen_udp(address=ADDRESS, port=PORT, dns=DNS, ca=CA_CERT):
    """Listening for DNS UDP requests"""
    print("udp listener")
    try:
        udp = UDP()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print("UDP SENT: ")
            print(data.decode("ISO-8859-1", "replace"))
            udp.handler(data, address=addr, socket=sock, dns_addr=dns, ca_path=ca)
    except Exception as e:
        print(e)
    finally:
        sock.close()


if __name__ == "__main__":
    listen_udp(ADDRESS, PORT, DNS, CA_CERT)
    listen_tcp(ADDRESS, PORT, DNS, CA_CERT)
