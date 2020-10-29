from socket import socket, AF_INET, SOCK_STREAM


class Server:
    def __init__(self, host, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

        while True:
            (self.client_socket, self.address_client) = self.server.accept()

            data = self.recv()
            self.send(data)


    def recv(self):
        data = self.client_socket.recv(2048)
        print(data.decode())
        return data

    def send(self, data):
        lista = data.decode().split(' ')
        path = ""
        path += lista[1][1:] # caminho do arquivo pesquisado pelo Browser sem o \
        status = 200

        try:
            arq = open(path, 'r')
            file = self.le_arquivo(arq)
        except FileNotFoundError:
            status = 404

        if status == 200:
            page = ('HTTP/1.1 200 OK\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Server: projetoredes/0.0.1 (Windows)\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
            page += file

        elif status == 404:
            page = ('HTTP/1.1 404 Not Found\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Server: projetoredes/0.0.1 (Windows)\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
            page += ('''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>404 not found</title>
                        </head>
                        <body>
                            404 error not found
                            sorry, this file wasn't found.
                        </body>
                        </html>''')

        self.client_socket.send(page.encode())

    def elimina_n(self, palavra):
        '''Elimina o \n'''
        nova_string = ""
        for caracter in palavra:
            nova_string += caracter
        return nova_string

    def le_arquivo(self, arquivo):
        '''Cria nova lista sem \n'''
        nova_string = ''

        for palavra in arquivo:
            nova_string += self.elimina_n(palavra)
        return nova_string

    def close(self):
        self.client_socket.close()


server = Server("localhost", 8080)
server.close()
