from threading import Thread
import time

def le_input():
    global acerto
    acerto = False

    print(pergunta[0])
    while(True):
        resposta = input("Resposta:")

        if resposta == pergunta[1]:
            break
        else:
            print("Resposta errada")
            acerto = False    
    acerto = True

pergunta = ("Pergunta: Quanto eh 1+1?\n","2")

for rodada in range(5):  #5 rodadas

    print("\nRODADA NO", rodada+1)

    t = Thread(target=le_input, daemon=True)  #Thread para clientes responderem a resposta (input())
    t.start()

    timer = 0
    while(True):
        if (timer==5):   
            print("\nTempo limite atingido")
            break

        if(acerto==False):
            time.sleep(1)  # +1 segundo
            timer+=1

        else:
            print("O jogador ____ acertou! Proxima pergunta -->")              #Dizer qual jogador acertou 
            break        
        
print("Acabou")