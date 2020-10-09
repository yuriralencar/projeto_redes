from socket import socket, AF_INET, SOCK_DGRAM

UDPClientSocket = socket(AF_INET, SOCK_DGRAM)

print("---------------------------------")
print("    BEM VINDO AO JOGUINHO        ")
print("Por, favor selecione a opção desejada: ")
print(" 1 - Iniciar Jogo ")
print(" 2 - Visualizar os maiores rankings ")
print("---------------------------------")

#Criação e envio da mensagem
mensagem_cliente = (input("Opção desejada: ")).encode()
UDPClientSocket.sendto(mensagem_cliente, ('localhost', 9500))

# Recebe resposta do servidor   ([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))
resposta_servidor = UDPClientSocket.recvfrom(1024)

msgServidor = resposta_servidor[0].decode()
ipServidor = resposta_servidor[1][0]

print((f'{msgServidor}'))  #Aguardando outros participantes...

def envia(mensagem):
    mensagem_cliente = mensagem.encode()
    UDPClientSocket.sendto(mensagem_cliente , ('localhost', 9500))
    

def partida():
    pass




for c in range(5):
    t = Thread(target=partida, daemon=True)  #Thread para partida
    t.start()

    
    resposta_servidor = UDPClientSocket.recvfrom(1024)
    msgServidor = resposta_servidor[0].decode()  #recebe pergunta

    print(f'{msgServidor}') #imprime pergunta
    
    envia(input("Digite sua resposta: "))   #envia resposta para servidor

    resposta_servidor = UDPClientSocket.recvfrom(1024)
    msgServidor = resposta_servidor[0].decode() #recebe avaliacao
    
    while True:
        if msgServidor == "400":  #resposta errada
            envia(input("Wrong answer.. tente novamente: "))

            resposta_servidor = UDPClientSocket.recvfrom(1024)
            msgServidor = resposta_servidor[0].decode()
            print("m",msgServidor)

        elif msgServidor == "500":
            print("Resposta correta. Próxima pergunta --> ")
            break

        elif msgServidor =="600":
            print("tle") ####
            break      

print("Fim de jogo! Mas tu é gay, para de negar!")   






