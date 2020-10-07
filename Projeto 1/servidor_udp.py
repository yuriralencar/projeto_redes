import time
from socket import socket, AF_INET, SOCK_DGRAM

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

#print("Servidor UDP escutando requisicoes")

listaJogadores = []
Pontuacao = []
while len(listaJogadores) < 1:

    #Recebe mensagem de cliente
    mensagem_cliente = UDPServerSocket.recvfrom(1024)

    data = mensagem_cliente[0].decode()
    endereco_cliente = mensagem_cliente[1]
    ip_cliente = mensagem_cliente[1][0]
    
    listaJogadores.append(endereco_cliente)
    Pontuacao.append(0)

    
    if data == "1":
        resposta_cliente = str.encode("Estamos procurando oponentes para você...")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
    elif data == "2":
        resposta_cliente = str.encode("Aqui está a lista com as maiores pontuações")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
    else:
        resposta_cliente = str.encode("Entrada inválida")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

#trabalhar com o arquivo de texto
pergunta = ("Tu é gay?", "GRAÇAS A DEUS")
for c in listaJogadores:
    resposta_cliente = str.encode(pergunta[0])
    UDPServerSocket.sendto(resposta_cliente, c)

mensagem_cliente = UDPServerSocket.recvfrom(1024)

data = mensagem_cliente[0].decode()
endereco_cliente = mensagem_cliente[1]

print(data)


