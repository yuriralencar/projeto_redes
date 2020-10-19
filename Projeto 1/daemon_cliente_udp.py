from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

parada = False
msgServidor = ""

UDPClientSocket = socket(AF_INET, SOCK_DGRAM)


def envia(mensagem):  # Criação e envio da mensagem
    mensagem_cliente = mensagem.encode()
    UDPClientSocket.sendto(mensagem_cliente, ('localhost', 9500))


def recebe():  # Thread
    global msgServidor

    while (True):
        resposta_servidor = UDPClientSocket.recvfrom(1024)  # ([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))
        msgServidor = str(resposta_servidor[0].decode())
        # print("\nRECEBEU:",msgServidor)
        time.sleep(1)


def partida():  # Thread 2
    global parada
    global msgServidor

    while (msgServidor == 'start' or msgServidor == '500' or msgServidor == '700' or msgServidor == '800'):
        pass

    pergunta = msgServidor

    print(pergunta)  # Imprime pergunta nº c+1

    envia(input("Insira sua resposta: "))  # responde ao servidor. funcao recebe() recebe avaliacao

    while (True):
        while (msgServidor == pergunta):
            pass

        if msgServidor == "400":
            envia(input("\nResposta incorreta.. tente novamente: "))
            time.sleep(1)

        elif msgServidor == "500" and c<4:
            print("\nResposta correta! Próxima pergunta --> ")
            break


print("---------------------------------")  ###Início do programa
print("    BEM VINDO AO JOGUINHO        ")
print("Por, favor selecione a opção desejada: ")
print(" 1 - Iniciar Jogo ")
print(" 2 - Visualizar os maiores rankings ")
print("---------------------------------")

envia(input("Opção desejada: "))

t = Thread(target=recebe, daemon=True)  # Thread para receber dados do servidor
t.start()

while (msgServidor == ''):
    pass

print(msgServidor)  # msgServidor = Aguardando outros participantes...

while (msgServidor != 'start'):
    # print(msgServidor,"msg")
    pass

print("Iniciando competicao...")  # Iniciando competicao...

for c in range(5):  # 5 partidas
    print("\npartida n:", c + 1)

    t2 = Thread(target=partida, daemon=True)  # Thread para cada partida
    t2.start()

    anterior = msgServidor

    while (True):
        if msgServidor == '500':
            time.sleep(2)
            break

        if msgServidor == '700':
            print("\nOutro jogador acertou")
            msgServidor = 'start'
            break

        elif msgServidor == '800':
            print("\nTempo esgotado")
            msgServidor = 'start'
            break

        else:
            time.sleep(0.7)

print("\nFim de jogo!")
exit(0)
