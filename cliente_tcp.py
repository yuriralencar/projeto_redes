from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class ClienteTCP:

    def __init__(self, endereco, porta):
        sock = socket(AF_INET, SOCK_STREAM)

        print('Tentando iniciar uma conexão com o servidor')
        sock.connect((endereco, porta))
        print('A conexão foi estabelida com sucesso.')

        Thread(target=self.receber_dados, args=(sock,)).start()

        while True:
            mensagem = input()

            sock.send(mensagem.encode())

    @staticmethod
    def receber_dados(sock):
        while True:
            dados = sock.recv(2048)

            print(f'Servidor enviou >>> {dados.decode()}')


cliente_tcp = ClienteTCP('172.23.0.6', 8080)
