from socket import socket, AF_INET, SOCK_STREAM
import os


class Server:
    def __init__(self, host, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.documentRoot = './diretorio'
        self.status = 200

        self.server.listen()

        if not os.path.exists(self.documentRoot):
            # cria diretório
            os.mkdir(self.documentRoot)

        while True:
            (self.client_socket, self.address_client) = self.server.accept()

            data = self.recv()
            self.send(data)

    def recv(self):
        data = self.client_socket.recv(2048)
        print(data.decode())
        return data

    def send(self, data):
        lista = data.decode().split(" ")
        path = self.documentRoot + lista[1]

        extensao = lista[1].split(".")
        extensao = extensao[1]
        comando = lista[0]

        if comando != "GET":
            self.status = 501

        if lista[1] == "/":
            path = self.documentRoot + "index.html"

        try:
            arq = open(path, 'rb')
            file = arq.read()
        except FileNotFoundError:
            self.status = 404

        if self.status == 501:
            page = ('HTTP/1.1 501 not implemented\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Allow: GET'
                    'Server: projetoredes/0.0.1 (Windows)\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
            page += ('''<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>501 not implemented</title>
                                    </head>
                                    <body>
                                        501 not implemented.
                                    </body>
                                    </html>''')
            newpage = page.encode()

        elif self.status == 404:
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
            newpage = page.encode()

        else:
            page = ('HTTP/1.1 200 OK\r\n'
                    f'Date: {os.path.getatime(path)}\r\n'
                    'Server: projetoredes/0.0.1 (Windows)\r\n'
                    'Content-Type: image/jpg\r\n'
                    f'Content-lenght: {os.path.getsize(path)}\r\n'
                    '\r\n')
            newpage = page.encode() + file

        self.client_socket.send(newpage)

    def close(self):
        self.client_socket.close()


server = Server("localhost", 8080)
server.close()
