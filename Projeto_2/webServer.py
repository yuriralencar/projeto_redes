from socket import socket, AF_INET, SOCK_STREAM
import os


class Server:
    def __init__(self, host, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.diretorio = os.getcwd()
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
        lista = data.decode().split(" ")
        path = self.diretorio + lista[1]

        extensao = lista[1].split(".")
        extensao = extensao[1]

        

        if lista[1] == "/":
            path = self.diretorio + "index.html"
            
        status = 200

        try:
            arq = open(path, 'rb')
            file = arq.read()
        except FileNotFoundError:
            status = 404
        
        if status == 200:
            page = ('HTTP/1.1 200 OK\r\n'
                    'Date: Wen 21 Oct 2020 12:10:30 GMT\r\n'
                    'Server: projetoredes/0.0.1 (Windows)\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
            newpage = page.encode() + file

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
            newpage = page.encode()



        self.client_socket.send(newpage)


    def close(self):
        self.client_socket.close()


server = Server("localhost", 8080)
server.close()
