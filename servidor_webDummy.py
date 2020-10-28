from socket import socket, AF_INET, SOCK_STREAM

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 9000))

while(True):
        
        server_socket.listen()
        client_socket, address_client = server_socket.accept()

        data = client_socket.recv(2048)
        dados = data.decode()

        dados = dados.split(" ")
        #print(dados)

        requisicao = dados[1]

        print("Browser requested:",requisicao)

        if(requisicao=="/favicon.ico"):
                pass


        msg = ('HTTP/1.1 200 OK\r\n'
        'Date: Thu, 24 Sep 2020 21:00:15 GMT\r\n'
        'Server: Dummy/0.0.1 (Ubuntu)\r\n'
        'Content-Type: text/html\r\n'
        '\r\n')

        msg += ('<html><head><title>AAAAAAA</title></head>'
                '<body><h1>Sei que arquivo eh esse nao porraaa</h1>'
                '<h3>inferno</h3>'
                '</body>'
                '</html>')

        client_socket.send(msg.encode())

        client_socket.close()
