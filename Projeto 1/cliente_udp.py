from socket import socket, AF_INET, SOCK_DGRAM

UDPClientSocket = socket(AF_INET, SOCK_DGRAM)

print("---------------------------------")
print("    BEM VINDO AO JOGUINHO        ")
print("Por, favor selecione a opção desejada: ")
print(" 1 - Iniciar Jogo ")
print(" 2 - Visualizar os maiores rankings ")
print("---------------------------------")
# Criação da mensagem a ser enviada
mensagem_cliente = (input("Opção desejada: ")).encode()

# Envia a mensagem para o servidor
UDPClientSocket.sendto(mensagem_cliente, ('localhost', 9500))

# Recebe resposta do servidor   ([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))
resposta_servidor = UDPClientSocket.recvfrom(1024)

msgServidor = resposta_servidor[0].decode()
ipServidor = resposta_servidor[1][0]

print((f'{msgServidor}'))

for c in range(5):
    resposta_servidor = UDPClientSocket.recvfrom(1024)
    msgServidor = resposta_servidor[0].decode()

    print(f'Pergunta {c+1}: ')
    print(f'{msgServidor}')

    mensagem_cliente = (input("Digite sua resposta: ")).encode()
    UDPClientSocket.sendto(mensagem_cliente, ('localhost', 9500))

    resposta_servidor = UDPClientSocket.recvfrom(1024)
    msgServidor = resposta_servidor[0].decode()

    while True:

        if msgServidor != "False":
            if msgServidor == "400":
                mensagem_cliente = (input("Wrong answer.. tente novamente: ")).encode()
                UDPClientSocket.sendto(mensagem_cliente, ('localhost', 9500))

                resposta_servidor = UDPClientSocket.recvfrom(1024)
                msgServidor = resposta_servidor[0].decode()
            else:
                if msgServidor == "500":
                    print("Resposta correta. Próxima pergunta --> ")
                else:
                    print("Fim de jogo! Mas tu é gay, para de negar!")
                break
        else:
            break

resposta_servidor = UDPClientSocket.recvfrom(1024)
msgServidor = resposta_servidor[0].decode()
print(msgServidor)

