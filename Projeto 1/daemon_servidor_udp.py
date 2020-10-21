from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

resposta = "0"
acerto = None
endereco_cliente = None

######Inicio do programa

print("Servidor UDP escutando requisicoes...")

listaJogadores = []
listaNomes = []
Pontuacao = []

quant_jogadores = 1

while len(listaJogadores) < quant_jogadores:  #Quantidade de jogadores

    #Recebe primeira mensagem de cliente (pedido de conexao)
    mensagem_cliente = UDPServerSocket.recvfrom(1024) #([0] = mensagem, [1] = endereco ([0]IP, [1]PORTA))

    data = mensagem_cliente[0].decode()
    endereco_cliente = mensagem_cliente[1]   #('192.168.0.1',84859)
    
    listaJogadores.append(endereco_cliente)
    listaNomes.append(data)
    Pontuacao.append(0)

    resposta_cliente = str.encode("\nAguardando outros participantes...\n")
    UDPServerSocket.sendto(resposta_cliente, endereco_cliente)


def envia_todos(mensagem): #Envia uma mensagem para todos os jogadores
    global listaJogadores

    for cliente in listaJogadores:  
        resposta_cliente = str.encode(mensagem)
        UDPServerSocket.sendto(resposta_cliente, cliente)

def num(number):
    if number % 2 == 0:
        return True
    else:
        return False


def elimina_n(palavra):
    '''Elimina o \n'''
    novaString = ""
    for caracter in palavra:
        if caracter != "\n":
            novaString += caracter
    return novaString


def le_arquivo(arquivo):
    '''Cria nova lista sem \n'''
    novaLista = []
    cont = 0
    tupla = ()
    for palavra in arquivo:
        cont += 1
        caracter = elimina_n(palavra)
        print(caracter)
        tupla1 = (caracter,)
        tupla += tupla1
        if num(cont):
            novaLista.append(tupla)
            tupla = ()
    return novaLista

def envia_resposta_errada(pular): #Envia uma mensagem para todos os jogadores
    global listaJogadores
    print("pull",pular)

    for cliente in listaJogadores:
        if cliente != pular:
            resposta_cliente = str.encode('900')
            UDPServerSocket.sendto(resposta_cliente, cliente)
        else:
            resposta_acerto = str.encode('500')  
            UDPServerSocket.sendto(resposta_acerto, endereco_cliente)
            

def recebe_mensagens():
    global resposta
    
    global endereco_cliente

    mensagem_cliente = UDPServerSocket.recvfrom(1024)  
    resposta = str(mensagem_cliente[0].decode())     #resposta dada pelo cliente
    endereco_cliente = mensagem_cliente[1]
    
    print("Recebeu",resposta,"de",endereco_cliente[0])


def partida():
    global resposta

    global acerto
    acerto = False

    envia_todos(listaPerguntas[k][0]) #Envia a pergunta para todos os jogadores

    while(True):
        recebe_mensagens()
        
        while(resposta=="0"):  
            time.sleep(0.1)

        if (resposta != listaPerguntas[k][1]): #Resposta errada

            resposta_cliente = str.encode("400")   
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] -= 5

            resposta = "0"
            acerto = False
                
        elif (resposta == listaPerguntas[k][1]): #Resposta correta

            #resposta_cliente = str.encode("500")  
            #UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

            envia_resposta_errada(endereco_cliente) #envia para o resto que errou

            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] += 25

            resposta = "0"
            acerto = True

            break


#trabalhar com arquivo de texto
#arquivo = open("projeto_redes.txt", "r")
#perguntas = le_arquivo(arquivo)
#arquivo.close()

#resposta_cliente = str.encode('start')
#UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

listaPerguntas = [('SIM', 'SIM'),('SIM', 'SIM'),('SIM', 'SIM'),('SIM', 'SIM'),('SIM', 'SIM')]

envia_todos('start')

time.sleep(2)

#t = Thread(target=recebe_mensagens, daemon=True)  #Thread para receber mensagens dos usuarios
#t.start()

resposta = "0"

for k in range(5):  #5 rodadas
    print("partida n:",k+1)

    t2 = Thread(target=partida, daemon=True)  #Thread para partida
    t2.start()

    tempo=0
    while(True):
        if(acerto):
            #resposta_cliente = str.encode('700')
            #UDPServerSocket.sendto(resposta_cliente, endereco_cliente) #envia para quem acertou
            print(endereco_cliente[0],"acertou")
            break
        
        if(tempo==5):   
            print("Tempo esgotado")
            envia_todos('800') #enviar para todo mundo
            break
        else:
            time.sleep(1)
            tempo+=1
            
    acerto = False

pontos = ""

for x in range(len(listaNomes)):

    pontos+= (listaNomes[x]+ " = " + str(Pontuacao[x]) + "\n")

envia_todos(pontos)

print("Fim")


