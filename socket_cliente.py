import socket

class SocketCliente:
    HOST = '127.0.0.1'
    PORT = 14340

    def __init__(self):
        # Definição de Objeto socktet INET STREAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associação do host e porta ao objeto socket
        self.sock.bind((SocketCliente.HOST, SocketCliente.PORT))

