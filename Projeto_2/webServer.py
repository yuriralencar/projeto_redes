from socket import socket, AF_INET, SOCK_STREAM
from mimetypes import guess_type
from datetime import datetime
import os


class Server:
    def __init__(self, host, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.documentRoot = os.getcwd()
        self.caminhoAtual = os.getcwd()
        self.html = ''
        self.status = 200

        self.server.listen()
        self.htmlPadrao()

        if not os.path.exists(self.documentRoot):
            # cria diretório
            os.mkdir(self.documentRoot)

        while True:
            try:
                (self.client_socket, self.address_client) = self.server.accept()

                data = self.recv()
                self.send(data)
            except IndexError:
                print("Erro")
                pass

    def recv(self):
        data = self.client_socket.recv(2048)
        print(data.decode())
        return data

    def send(self, data):
        lista = data.decode().split(" ")
        version = lista[2][5:8]  # versão do http
        caminho = self.documentRoot
        if lista[1] != '/favicon.ico':
            caminho = self.documentRoot + lista[1]
        comando = lista[0]

        for caracter in caminho:
            if caracter == ' ':
                self.status = 400

        if comando != "GET":
            self.status = 501

        if version != '1.1' and version != '1.0':
            self.status = 505

        try:
            if os.path.isdir(caminho):
                document_root_split = self.documentRoot.split('/')
                # caminhos dos arquivos de 'caminho'
                caminhos = [os.path.join(caminho, nome) for nome in os.listdir(caminho)]
                for p in caminhos:
                    caminho_split = p.split('/')
                    flag = False
                    caminho_atual = ''
                    for arquivo in caminho_split:
                        if flag:
                            caminho_atual += ('/' + arquivo)
                        elif arquivo == document_root_split[-1]:
                            flag = True
                    stamp = os.path.getmtime(p)
                    dt_object = datetime.fromtimestamp(stamp)
                    if not os.path.isdir(p):
                        self.html += f'''
                                <tr>
                                    <td><a href= {f'{caminho_atual}'}>{os.path.basename(p)}</td>
                                    <td align= "right">{dt_object}</td>
                                    <td align= "right">{os.path.getsize(p)}</td>
                                    <td>&nbsp;</td>
                                </tr>
                        '''

                    else:

                        self.html += f'''
                                <tr>
                                    <td><a href= {f'{caminho_atual}'}>{os.path.basename(p)}</td>
                                    <td align= "right">{dt_object}</td>
                                    <td align= "right"></td>
                                    <td>&nbsp;</td>
                                </tr>
                        '''

                self.html += '''
                        </table>
                        <h3>Servidor do Tchan.</h3>
                    </body>
                    </html>
                '''
                file = self.html.encode()
                self.htmlPadrao()
            else:
                print(caminho)
                arq = open(caminho, 'rb')
                file = arq.read()
                arq.close()
        except FileNotFoundError:
            self.status = 404

        if self.status == 501:
            page = ('HTTP/1.1 501 not implemented\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Allow: GET'
                    'Server: servidordotchan/0.0.1 (Windows)\r\n'
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
                        <h1>501 not implemented.</h1>
                    </body>
                    </html>''')
            newpage = page.encode()
            self.status = 200

        elif self.status == 505:
            page = ('HTTP/1.1 505 HTTP Version Not Supported\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Server: servidordotchan/0.0.1 (Windows)\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
            page += ('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>505 HTTP Version Not Supported</title>
                    </head>
                    <body>
                        <h1>505 HTTP Version Not Supported</h1>
                    </body>
                    </html>''')
            newpage = page.encode()
            self.status = 200

        elif self.status == 400:
            page = ('HTTP/1.1 400 Bad Request\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Server: servidordotchan/0.0.1 (Windows)\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
            page += ('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>400 Bad Request</title>
                    </head>
                    <body>
                        <h1>400 Bad Request</h1>
                    </body>
                    </html>''')
            newpage = page.encode()
            self.status = 200

        elif self.status == 404:
            page = ('HTTP/1.1 404 Not Found\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Server: servidordotchan/0.0.1 (Windows)\r\n'
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
                            <h1>404 error not found</h1>
                            sorry, this file wasn't found.
                        </body>
                        </html>''')
            newpage = page.encode()
            self.status = 200

        else:
            page = ('HTTP/1.1 200 OK\r\n'
                    f'Date: {os.path.getatime(caminho)}\r\n'
                    'Server: servidordotchan/0.0.1 (Windows)\r\n'
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
            '''

    def close(self):
        print("Servidor WEB finalizado")
        self.client_socket.close()


print("Servidor WEB ouvindo requisições\n\n")
server = Server("192.168.1.65", 8080)