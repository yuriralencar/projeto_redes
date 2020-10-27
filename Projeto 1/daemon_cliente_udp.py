from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

parada = False
msgServidor_cliente = ''  # msg do servidor para o cliente
msgServidor_thread = ''  # msg do servidor pro sistema gerenciar threads

UDPClientSocket = socket(AF_INET, SOCK_DGRAM)


def envia(mensagem):  # Criação e envio da mensagem
    mensagem_cliente = mensagem.encode()
    UDPClientSocket.sendto(mensagem_cliente, ('192.168.1.91', 9500))


def recebe():  # Thread
    global msgServidor_cliente
    global msgServidor_thread

    while (True):
        resposta_servidor = UDPClientSocket.recvfrom(
            1024)  # ([0] = mensagem: [0]continua thread (Cliente/Thread) , [1]DADOS)/([1] / endereco: ([0]IP, [1]PORTA)
        resposta = str(resposta_servidor[0].decode())

        status_cliente = ''
        mensagem = ''

        for x in resposta:
            if (x == '&'):
                status_cliente = mensagem
                mensagem = ''
            else:
                mensagem += x

        if (status_cliente == 'Thread'):
            msgServidor_thread = mensagem
        else:
            msgServidor_cliente = mensagem


def partida():  # Thread 2
    global parada
    global msgServidor_cliente

    while (msgServidor_cliente == ''):  # Aguarda servidor enviar pergunta
        time.sleep(0.1)

    pergunta = msgServidor_cliente
    print("\nPartida nº", c + 1, "\nPergunta:", pergunta)  # Imprime pergunta nº c+1

    resposta = input("Insira sua resposta: ")

    envia('Cliente1&' + resposta)  # responde ao servidor. funcao recebe() recebe avaliacao

    while (True):  # fica preso aqui ate acertar ou a thread ser quebrada
        if msgServidor_cliente == "400":
            msgServidor_cliente = ''
            resposta = input("Resposta incorreta.. tente novamente: ")
            envia('Cliente1&' + resposta)
        else:
            time.sleep(0.1)


print("---------------------------------")  ###Início do programa
print("    BEM VINDO AO JOGUINHO        ")
print("Para iniciar, digite seu nome!")

nome = input("Nome:")

while (nome == ''):
    nome = input("Nome inválido, tente novamente:")

envia('Cliente0&' + nome)

t = Thread(target=recebe, daemon=True)  # Thread para receber dados do servidor
t.start()

while msgServidor_cliente == '':
    time.sleep(0.1)

if (msgServidor_cliente == 'JaIniciou'):
    print("Partida Já Iniciou. Tente novamente em instantes")
    input("Pressione qualquer tecla para finalizar")
    exit(0)

print(msgServidor_cliente)  # msgServidor_cliente = Aguardando outros participantes...

while (msgServidor_cliente != 'start'):  # Aguarda servidor enviar comando para inicio
    time.sleep(0.1)

msgServidor_cliente = ''
print("Iniciando competicao...")  # Iniciando competicao...

for c in range(5):  # 5 partidas
    t2 = Thread(target=partida, daemon=True)  # Thread para cada partida
    t2.start()

    while (True):
        if msgServidor_cliente == '500' and c < 4:
            msgServidor_cliente = ''
            print("\nResposta correta! Próxima pergunta --> ")
            break

        if msgServidor_thread == '900':
            msgServidor_thread = ''
            msgServidor_cliente = ''
            print("\nOutro jogador acertou")
            break

        elif msgServidor_thread == '800':
            msgServidor_thread = ''
            msgServidor_cliente = ''
            print("\nTempo esgotado")
            break
        else:
            time.sleep(0.1)

print("\nFim de jogo! Pontuações da partida:")

resposta_servidor = UDPClientSocket.recvfrom(1024)  # ([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))
msgServidor = str(resposta_servidor[0].decode())
print(msgServidor)

print("Deseja jogar novamente?")
