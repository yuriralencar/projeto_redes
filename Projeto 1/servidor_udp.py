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

for k in range(0,5):
    
    print(k)

    pergunta = ("Tu é gay?", "NAO")

    for c in listaJogadores:
        resposta_cliente = str.encode(pergunta[0])
        UDPServerSocket.sendto(resposta_cliente, c)

    cond = True
    while cond:
        mensagem_cliente = UDPServerSocket.recvfrom(1024)
        data = mensagem_cliente[0].decode()
        endereco_cliente = mensagem_cliente[1]

        if data != pergunta[1]:
            resposta_cliente = str.encode("400")
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] -= 5
        elif data == pergunta[1]:
            if k == 4:
                print("aqui")
                resposta_cliente = str.encode("600")
            else:
                resposta_cliente = str.encode("500")
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
            acertou = endereco_cliente
            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] += 25
            break


for c in listaJogadores:
    resposta_cliente = str.encode("False")
    UDPServerSocket.sendto(resposta_cliente, c)

print(Pontuacao)


