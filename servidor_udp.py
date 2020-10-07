import time
from socket import socket, AF_INET, SOCK_DGRAM

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

#print("Servidor UDP escutando requisicoes")

while(True):

    listaJogadores = []
    Pontuacao = []

    data = mensagem_cliente[0].decode()
    endereco_cliente = mensagem_cliente[1]
    ip_cliente = mensagem_cliente[1][0]

    end_time = time.time() + 10
    countTimer = 0
    sleepTime = 1
    while (len(listaJogadores) < 2) or (time.time() < end_time):

        #Recebe mensagem de cliente
        mensagem_cliente = UDPServerSocket.recvfrom(1024)
        time.sleep(sleepTime)
        countTimer += sleepTime
        listaJogadores.append(ip_cliente)
        Pontuacao.append(0)
    

    print(listaJogadores)




    
    print(" ")
    print((f'O cliente ({ip_cliente}) enviou: {data}'))

    #Responde para cliente
    resposta_cliente = str.encode("Mensagem recebida com sucesso")
    UDPServerSocket.sendto(resposta_cliente, endereco_cliente)