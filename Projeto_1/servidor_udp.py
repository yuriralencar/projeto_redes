from socket import socket, AF_INET, SOCK_DGRAM


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


# Criacao do socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('localhost', 9500))

# print("Servidor UDP escutando requisicoes")

print("procurando por conexões...")


listaJogadores = []
Pontuacao = []
while True:

    # Recebe mensagem de cliente
    mensagem_cliente = UDPServerSocket.recvfrom(1024)

    data = mensagem_cliente[0].decode()
    endereco_cliente = mensagem_cliente[1]
    ip_cliente = mensagem_cliente[1][0]
    print(f'Jogador {endereco_cliente} conectado!')

    listaJogadores.append(endereco_cliente)
    Pontuacao.append(0)

    if data == "1":
        resposta_cliente = str.encode("Estamos procurando oponentes para você...")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
        break
    elif data == "2":
        resposta_cliente = str.encode("Aqui está a lista com as maiores pontuações")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
    else:
        resposta_cliente = str.encode("Entrada inválida")
        UDPServerSocket.sendto(resposta_cliente, endereco_cliente)

# trabalhar com o arquivo de texto

for k in range(0, 5):

    print(k)
    arquivo = open("projeto_redes.txt", "r")
    perguntas = le_arquivo(arquivo)
    print(perguntas)
    arquivo.close()

    for c in listaJogadores:
        resposta_cliente = str.encode(perguntas[k][0])
        UDPServerSocket.sendto(resposta_cliente, c)

    cond = True
    while cond:
        mensagem_cliente = UDPServerSocket.recvfrom(1024)
        data = mensagem_cliente[0].decode()
        endereco_cliente = mensagem_cliente[1]

        if data != perguntas[k][1]:
            resposta_cliente = str.encode("400")
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] -= 5
        elif data == perguntas[k][1]:
            if k == 4:
                print("aqui")
                resposta_cliente = str.encode("600")
            else:
                resposta_cliente = str.encode("500")
            UDPServerSocket.sendto(resposta_cliente, endereco_cliente)
            acertou = endereco_cliente
            posicao = listaJogadores.index(endereco_cliente)
            Pontuacao[posicao] += 25
            cond = False


mensagem_cliente = ''
cont = 0
for pos in Pontuacao:
    cont += 1
    mensagem_cliente += str(cont) + ' -> ' + str(pos)
resposta_cliente = str.encode(mensagem_cliente)
for cliente in listaJogadores:
    print(mensagem_cliente)
    UDPServerSocket.sendto(resposta_cliente, cliente)



