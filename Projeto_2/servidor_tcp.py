from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class ServidorTCP:
    def __init__(self, endereco, porto):
        socket_servidor = socket(AF_INET, SOCK_STREAM)

        socket_servidor.bind((endereco, porto))

        socket_servidor.listen()

        print('Aguardando novas requisições chegarem.')

        while True:
            (socket_cliente, endereco_cliente) = socket_servidor.accept()
            print(f'A requisição com o cliente {endereco_cliente} foi estabelecida.')

            Thread(target=self.receber_dados, args=(socket_cliente, endereco_cliente)).start()

    @staticmethod
    def receber_dados(socket_cliente, endereco_cliente):
        while True:
            dados = socket_cliente.recv(2048)

            print(f'O cliente {endereco_cliente} enviou >>> {dados.decode()}')

            socket_cliente.send('Recebi sua mensagem com sucesso!'.encode())


servidor_tcp = ServidorTCP('150.161.2.147', 8080)
