import socket
from tinydb import TinyDB, Query

HOST = '127.0.0.1'
PORT = 14340

#Definição de Objeto socktet INET STREAM
db_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Associação do host e porta ao objeto socket
db_socket_server.bind((HOST, PORT))
#Tornando em um server socket
db_socket_server.listen()


#Enquanto o server estiver up ele deverá aceitar a conexão de quaisquer cliente
while True: #loop de conexão
    #Aceitando a conexão com o cliente
    conexao, endereco_cliente = db_socket_server.accept()
    print('Cliente', endereco_cliente)

    #Os dados devem ser recebidos até que se complete a mensagem
    while True: #loop de recebimento
        dados = conexao.recv(1024)
        if not dados:
            break

        conexao.sendall(dados)

    conexao.close()

db_socket_server.close()