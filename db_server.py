import socket
import db
import json
from socket_interface import SocketInterface


def encaminha(msg):

    if msg["tipo_query"] == 'busca_livros':
        return db.buscar_livros()

    if msg["tipo_query"] == 'busca_livro':
        return db.buscar_livro(msg["parametro"])

    if msg["tipo_query"] == 'inserir_livro':
        return db.inserir_livro(msg["parametro"])

    if msg["tipo_query"] == 'altera_livro':
        return db.altera_livro(msg["parametro"]["id"], msg["parametro"])

    if msg["tipo_query"] == 'deleta_livro':
        return db.deleta_livro(msg["parametro"])

    if msg["tipo_query"] == 'deleta_livros':
        return db.deleta_livros()


class SocketServer(SocketInterface):

    HOST = '127.0.0.1'
    PORT = 14340

    def __init__(self):
        # Definição de Objeto socktet INET STREAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associação do host e porta ao objeto socket
        self.sock.bind((SocketServer.HOST, SocketServer.PORT))
        self.conec_associada = None
        self.endereco_associado = None

    def start(self):
        self.sock.listen()
        while True:
            self.conec_associada, self.endereco_associado = self.sock.accept()
            retorno = self.receive()
            self.send(msg=retorno)
            print(encaminha(json.loads(retorno)))
            self.conec_associada.close()

    def receive(self) -> bytes:
        partes = []
        while True:
            dados = self.conec_associada.recv(1024)
            if not dados:
                break
            partes.append(dados)

        return b''.join(partes)

    def send(self, msg) -> None:
        return self.sock.sendall(msg)


MeuSocket = SocketServer()
print(dir(MeuSocket))
MeuSocket.start()

teste1 = {"tipo_query": 'get_livros'}

teste2 = {"tipo_query": 'get_livros', "parametro": 1}

teste3 = {"tipo_query": 'inserir_livro',
          "parametro": {"id": 1,
                         "titulo": "Senhor dos aneis",
                         "preco": 50}
          }

teste4 = {"tipo_query": 'altera_livro',
          "parametro": {"id": 1,
                         "titulo": "Senhor dos aneis",
                         "preco": 50}
          }

teste5 = {"tipo_query": 'deleta_livro', "parametro": 1}

teste6 = {"tipo_query": 'deleta_livros'}
