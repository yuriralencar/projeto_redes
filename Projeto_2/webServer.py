from socket import socket, AF_INET, SOCK_STREAM
from mimetypes import guess_type
import os


class Server:
    def __init__(self, host, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.documentRoot = 'C:/users/vinny/pycharm/py/redes/servidor_tcp/projeto2/diretorio'
        self.html = ''
        self.status = 200

        self.server.listen()
        self.htmlPadrao()

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
        caminho = self.documentRoot + lista[1]
        if os.path.isdir(caminho):
            caminhos = [os.path.join(caminho, nome) for nome in os.listdir(caminho)]
            for p in caminhos:
                print(p)

        comando = lista[0]

        if comando != "GET":
            self.status = 501

        if lista[1] == "/":
            caminho = self.documentRoot + "index.html"

        try:
            arq = open(caminho, 'rb')
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
            page += ('''
                    <!DOCTYPE html>
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
            page += ('''
                        <!DOCTYPE html>
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
                    f'Date: {os.path.getatime(caminho)}\r\n'
                    'Server: projetoredes/0.0.1 (Windows)\r\n'
                    f'Content-Type: {guess_type(caminho)[0]}\r\n'
                    f'Content-lenght: {os.path.getsize(caminho)}\r\n'
                    '\r\n')
            newpage = page.encode() + file

        self.client_socket.send(newpage)

    def htmlPadrao(self):
        self.html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Index of /</title>
        </head>
        <body>
            <h1>Index of /</h1>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Last Modified</th>
                    <th>Size</th>
                    <th>Description</th>
                </tr>
            </table>

        </body>
        </html>'''

    def close(self):
        self.client_socket.close()


server = Server("localhost", 8080)
server.close()
