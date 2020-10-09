from socket import socket, AF_INET, SOCK_DGRAM

UDPClientSocket = socket(AF_INET, SOCK_DGRAM)

while(True):

    print(" ")
    #Criação da mensagem a ser enviada
    mensagem_cliente = (input("Enviar para o servidor: ")).encode()


    #Envia a mensagem para o servidor
    UDPClientSocket.sendto(mensagem_cliente, ('172.23.0.6', 9500))

    #Recebe resposta do servidor   ([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))
    resposta_servidor = UDPClientSocket.recvfrom(1024)

    msgServidor = resposta_servidor[0].decode()
    ipServidor = resposta_servidor[1][0]

    print((f'O servidor {ipServidor} respondeu: {msgServidor}'))


#teesteeee