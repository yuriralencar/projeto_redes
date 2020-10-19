from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

resposta = "0"
acerto = None

######Inicio do programa

print("Servidor UDP escutando requisicoes...")

listaJogadores = []
Pontuacao = []

quant_jogadores = 1

while len(listaJogadores) < quant_jogadores:  #Quantidade de jogadores

    #Recebe primeira mensagem de cliente (pedido de conexao)
    mensagem_cliente = UDPServerSocket.recvfrom(1024) #([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))

    data = mensagem_cliente[0].decode()
    endereco_cliente = mensagem_cliente[1]
    
    listaJogadores.append(endereco_cliente)
    Pontuacao.append(0)

    if data == "1":
        resposta_cliente = str.encode("\nAguardando outros participantes...\n")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
    elif data == "2":
        resposta_cliente = str.encode("Aqui está a lista com as maiores pontuações")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
    else:
        resposta_cliente = str.encode("Entrada inválida")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

def envia_todos(mensagem): #Envia uma mensagem para todos os jogadores
    global listaJogadores

    for cliente in listaJogadores:  
        resposta_cliente = str.encode(mensagem)
        UDPServerSocket.sendto(resposta_cliente, cliente)

def envia_resposta_errada(mensagem, pular): #Envia uma mensagem para todos os jogadores
    global listaJogadores

    for cliente in listaJogadores: 
        if cliente != pular: 
            resposta_cliente = str.encode(mensagem)
            UDPServerSocket.sendto(resposta_cliente, cliente)


def recebe_mensagens():
    global resposta

    while(True):
        mensagem_cliente = UDPServerSocket.recvfrom(1024)  
        resposta = str(mensagem_cliente[0].decode())     #resposta dada pelo cliente
        endereco_cliente = mensagem_cliente[1]
        print("Recebeu",resposta,"de",endereco_cliente[0])


def partida():
    global resposta

    global acerto
    acerto = False

    envia_todos(listaPerguntas[k][0]) #Envia a pergunta para todos os jogadores

    #for c in listaJogadores:  
    #    resposta_cliente = str.encode(listaPerguntas[k][0])
    #    UDPServerSocket.sendto(resposta_cliente, c)  #c = (ip_cliente, porta_cliente) 

    while(True):
        while(resposta=="0"):  #mensagem modificada na funcao recebe_mensagens
            time.sleep(0.1)

        if (resposta != listaPerguntas[k][1]): #Resposta errada

            resposta_cliente = str.encode("400")   
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] -= 5

            resposta = "0"
            acerto = False
                
        elif (resposta == listaPerguntas[k][1]): #Resposta correta

            resposta_cliente = str.encode("500")  
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)


            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] += 25

            resposta = "0"
            acerto = True

            break


#trabalhar com arquivo de texto
listaPerguntas = [('Pergunta no 1','1'),('Pergunta no 2','2'),('Pergunta no 3','3'),('Pergunta no 4','4'),('Pergunta no 5','5')]

#resposta_cliente = str.encode('start')
#UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

envia_todos('start')

time.sleep(2)


t = Thread(target=recebe_mensagens, daemon=True)  #Thread para receber mensagens dos usuarios
t.start()

resposta = "0"

for k in range(5):  #5 rodadas
    print("partida n:",k+1)

    t2 = Thread(target=partida, daemon=True)  #Thread para partida
    t2.start()

    tempo=0
    while(True):
        if(acerto):
            resposta_cliente = str.encode('700')
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente) #envia para quem acertou
            envia_resposta_errada('900', endereco_cliente) #envie para o resto que errou
            print(endereco_cliente[0],"acertou")
            acerto = False
            break
        if(tempo==10):   
            print("Tempo esgotado")
            envia_todos('800') #enviar para todo mundo
            break
        else:
            time.sleep(1)
            tempo+=1

print(Pontuacao)

exit(0)  #coloquei isso na tentativa de parar o erro que aparece depois
         #de exibir a pontuacao pois a thread foi quebrada