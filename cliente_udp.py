from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

while True:
    mensagem = input()
    sock.sendto(mensagem.encode(), ('localhost', 9500))

# sock.close()
