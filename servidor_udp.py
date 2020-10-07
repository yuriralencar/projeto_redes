from socket import socket, AF_INET, SOCK_DGRAM

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('192.168.1.65', 9500))

#print("Servidor UDP escutando requisicoes")

while(True):

    #Recebe mensagem de cliente
    mensagem_cliente = UDPServerSocket.recvfrom(1024)

    #mensagem_cliente = (mensagem em bytes,(ip_cliente,porta))
    listaJogadores = []
    Pontuacao = []

    data = mensagem_cliente[0].decode()
    endereco_cliente = mensagem_cliente[1]
    ip_cliente = mensagem_cliente[1][0]

    if ip_cliente not in listaJogadores:
        listaJogadores.append(ip_cliente)
        Pontuacao.append(0)
    

    print(listaJogadores)




    
    print(" ")
    print((f'O cliente ({ip_cliente}) enviou: {data}'))

    #Responde para cliente
    resposta_cliente = str.encode("Mensagem recebida com sucesso")
    UDPServerSocket.sendto(resposta_cliente, endereco_cliente)