from socket import socket, AF_INET, SOCK_DGRAM

server_socket = socket(AF_INET, SOCK_DGRAM)

server_socket.bind(('172.23.30.241', 9500))

# server_socket.listen()

while True:
    data, client_adress = server_socket.recvfrom(2048)

    print(f'O cliente {client_adress} mandou >>> {data.decode()}')
