from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

resposta_cadastrado = ''
resposta_nao_cadastrado = ''

endereco_cliente_cad = None
endereco_cliente_nao_cad = None

acerto = None
ja_iniciou = False

def recebe_mensagens():
    global resposta_cadastrado
    global resposta_nao_cadastrado
    global endereco_cliente_cad
    global endereco_cliente_nao_cad
    global ja_iniciou

    while(True):
        mensagem_cliente = UDPServerSocket.recvfrom(1024)   #((Cliente1,Mensagem),(IP,Porta))
        msg = str(mensagem_cliente[0].decode())     #resposta dada pelo cliente
        end = mensagem_cliente[1]  #('192.168.0.1',84859)

        status_cliente = ''
        mensagem = ''

        for x in msg:
            if (x == '&'):
                status_cliente = mensagem
                mensagem = ''
            else:
                mensagem += x

        print("Recebeu",mensagem,"de",end[0])

        if(status_cliente=="Cliente1"):
            resposta_cadastrado = mensagem
            endereco_cliente_cad =  end

        elif(status_cliente=="Cliente0" and ja_iniciou):
            resposta_cliente = str.encode('Cliente0&'+'JaIniciou')
            UDPServerSocket.sendto(resposta_cliente, end)
            print("\nAlguem nao cadastrado tentou se conectar\n")

        else:
            resposta_nao_cadastrado = mensagem
            endereco_cliente_nao_cad =  end


def envia_todos(mensagem, status): #Envia uma mensagem para todos os jogadores
    global listaJogadores    #status = Cliente1/Thread

    for cliente in listaJogadores:  #cliente = (IP, Porta)
        resposta_cliente = str.encode(status+mensagem)
        UDPServerSocket.sendto(resposta_cliente, cliente)

def envia_resposta_errada(pular): #Envia uma mensagem para todos os jogadores que nao acertaram
    global listaJogadores

    for cliente in listaJogadores:
        if cliente != pular:
            resposta_cliente = str.encode('Thread&'+'900')
            UDPServerSocket.sendto(resposta_cliente, cliente)
        else:
            resposta_acerto = str.encode('Cliente1&'+'500')  
            UDPServerSocket.sendto(resposta_acerto, pular)
            
def partida():
    global acerto
    global resposta_cadastrado
    global endereco_cliente_cad
    global ja_iniciou

    acerto = False

    envia_todos(listaPerguntas[k][0],'Cliente1&') #Envia a pergunta para todos os jogadores

    while(True):
        if (ja_iniciou==False):
            break

        while(resposta_cadastrado==''):  
            time.sleep(0.1)

        if ja_iniciou==False:
            break

        if (resposta_cadastrado != listaPerguntas[k][1]): #Resposta errada

            resposta_cliente = str.encode('Cliente1&'+'400')   
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente_cad)

            posicao = listaJogadores.index(endereco_cliente_cad)
            pontuacao[posicao] -= 5

            resposta_cadastrado = ''
            acerto = False
                
        elif (resposta_cadastrado == listaPerguntas[k][1] and acerto==False): #Resposta correta

            print(endereco_cliente_cad[0],"acertou")
            envia_resposta_errada(endereco_cliente_cad) #envia para o resto que errou

            posicao = listaJogadores.index(endereco_cliente_cad)
            pontuacao[posicao] += 25

            resposta_cadastrado = ''
            acerto = True

            break

######## Inicio do programa (main()) #######

t = Thread(target=recebe_mensagens, daemon=True)  #Thread para receber mensagens dos usuarios
t.start()

print("Servidor UDP escutando requisicoes...")

listaJogadores = []
listaNomes = []
pontuacao = []

quant_jogadores = 1

continua = True

while(continua):
    while len(listaJogadores) < quant_jogadores:  #Quantidade de jogadores

        #Recebe primeira mensagem de cliente (pedido de conexao)
        while(resposta_nao_cadastrado==''):
            time.sleep(0.1)

        listaNomes.append(resposta_nao_cadastrado)
        listaJogadores.append(endereco_cliente_nao_cad)
        pontuacao.append(0)

        resposta_cliente = str.encode(('Cliente1&\nAguardando outros participantes...\n'))
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente_nao_cad)

        resposta_nao_cadastrado=''

    time.sleep(1) # Aguarda todos receberem a mensagem "Aguardando outros participantes...")

    listaPerguntas = [('Pergunta 1', '1'),('Pergunta 2', '2'),('Pergunta 3', '3'),('Pergunta 4', '4'),('Pergunta 5', '5')]

    comandoInicio = 'start'

    envia_todos(comandoInicio,'Cliente1&')

    print("\nIniciando competição...")

    time.sleep(1)  #espera todos receberem o comando de start

    resposta = ''

    ja_iniciou = True

    for k in range(5):  #5 rodadas

        time.sleep(3) #Aguarda todos reiniciarem suas partidas

        print("\nPartida nº:",k+1)

        t2 = Thread(target=partida,daemon=True)  #Thread para partida
        t2.start()

        tempo=0
        while(True):
            if(acerto):
                acerto = False
                break
            
            if(tempo==3):   
                print("Tempo esgotado")
                envia_todos('800','Thread&') #enviar para todo mundo
                for x in range(len(pontuacao)):
                    pontuacao[x]-=1
                break
            else:
                time.sleep(1)
                tempo+=1
        resposta_cadastrado = ''
        endereco_cliente_cad= ''

    pontos = ''

    for x in range(len(listaNomes)):
        pontos+= (listaNomes[x]+" = "+ str(pontuacao[x]) +"\n")

    print("\nFim de Jogo! Pontuacoes da partida:")
    print(pontos)

    time.sleep(1) #aguarda todos ouvirem a pontuacao

    envia_todos(pontos,'Thread&')

    ja_iniciou = False
    listaJogadores=[]
    listaNomes = []
    pontuacao = []
    resposta_cadastrado=''
    resposta_nao_cadastrado=''

    print("\nServidor UDP escutando requisições...")


print("Após 20 segundos ninguém se conectou...\nServidor finalizado!")
