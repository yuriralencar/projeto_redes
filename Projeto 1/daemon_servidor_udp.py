from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

#Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

print("Servidor UDP escutando requisicoes...")

listaJogadores = []
Pontuacao = []
while len(listaJogadores) < 1:  #Quantidade de jogadores

    #Recebe mensagem de cliente
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

def partida():
    global acerto 
    acerto = False

    for c in listaJogadores:  #Envia a pergunta para todos os jogadores
        resposta_cliente = str.encode(listaPerguntas[k][0])
        UDPServerSocket.sendto(resposta_cliente, c)  #c = (ip_client, porta_client)

    while(True):
        mensagem_cliente = UDPServerSocket.recvfrom(1024)  
        data = mensagem_cliente[0].decode()     #resposta dada pelo cliente
        endereco_cliente = mensagem_cliente[1]

        if (data != listaPerguntas[k][0]): #Resposta errada
            resposta_cliente = str.encode("400")   
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] -= 5
            acerto = False
            
        elif (data == listaPerguntas[k][0]): #Resposta correta
            resposta_cliente = str.encode("500")  
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] += 25
            acerto = True
            break

#trabalhar com o arquivo de texto
listaPerguntas = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]

for k in range(5):  #5 rodadas
    t = Thread(target=partida, daemon=True)  #Thread para partida
    t.start()

    timer = 0
    while(True):
        if (timer==5):   
            print("\nTempo limite excedido\n")
            break                                         

        if(acerto==False):
            time.sleep(1)  # +1 segundo
            timer+=1

        else:
            print(f"\nO jogador {endereco_cliente} acertou! \nProxima pergunta -->\n")              #Dizer qual jogador acertou
            break
        

        
print(Pontuacao)


