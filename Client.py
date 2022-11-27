import socket
import Document as doc

HOST = "192.168.8.105"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def sendIt(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(message))


def sendData(message):
    sendIt(message)
    doc.removeitself()