import socket
import db
import json

def encaminha(msg):

    if msg["tipo_query"] == 'busca_livros':
        return db.buscar_livros()

    if msg["tipo_query"] == 'busca_livro':
        return db.buscar_livro(msg["parametro"])

    if msg["tipo_query"] == 'inserir_livro':
        return db.inserir_livro(msg["parametro"])

    if msg["tipo_query"] == 'altera_livro':
        return db.altera_livro(msg["parametro"]["id"] ,msg["parametro"])

    if msg["tipo_query"] == 'deleta_livro':
        return db.deleta_livro(msg["parametro"])

    if msg["tipo_query"] == 'deleta_livros':
        return db.deleta_livros()


def uni_msg(partes_msg):

    msg_final = ''
    for parte in partes_msg:
        msg_final += parte.decode()
    print(msg_final)
    return json.loads(msg_final)


class SocketServer:
    HOST = '127.0.0.1'
    PORT = 14340

    def __init__(self):
        print("Aa")
        # Definição de Objeto socktet INET STREAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associação do host e porta ao objeto socket
        self.sock.bind((SocketServer.HOST, SocketServer.PORT))

    def start(self):
        self.sock.listen()
        while True:
            self.conec_associada, self.endereco_associado  =  self.sock.accept()
            retorno = uni_msg(self.severreceive())
            print(encaminha(retorno))
            self.conec_associada.close()

    def severreceive(self):
        partes = []
        while True:
            dados = self.conec_associada.recv(1024)
            if not dados:
                break
            partes.append(dados)

        return  partes


MeuSocket = SocketServer()
print(dir(MeuSocket))
MeuSocket.start()

teste1 = {"tipo_query" : 'get_livros'}

teste2 = {"tipo_query" : 'get_livros', "parametro" : 1}

teste3 = {"tipo_query" : 'inserir_livro',
          "parametro" : {"id" : 1,
                         "titulo" : "Senhor dos aneis",
                         "preco" : 50}
          }

teste4 = {"tipo_query" : 'altera_livro',
          "parametro" : {"id" : 1,
                         "titulo" : "Senhor dos aneis",
                         "preco" : 50}
          }

teste5 = {"tipo_query" : 'deleta_livro', "parametro" : 1}

teste6 = {"tipo_query" : 'deleta_livros'}
