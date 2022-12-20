import socket
import threading
import time


files = ['1', '2', '3', '4', '5', '6', '7', '8']
columnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

clients = []
llista_cua = []
en_cua = 0
rival1 = []
rival2 = []

def main(self):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)
    print("Escriu adreça del host:")
    HOST_ADDR = input()
    print("Escriu port del host:")
    HOST_PORT = input()
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen()
    acceptar_clients(server)

#Mira si hi ha més de 2 jugadors en cua i els ajunta
def matchMaking(self):

    if (en_cua >= 2):

        print ("Matchmaking 2 jugadors")
        #Posem els dos jugadors un a cada vector de rivals (tindran mateix índex)
        rival1.append(llista_cua.pop(0))
        rival2.append(llista_cua.pop(0))
        indx = len(rival1)
        msg_blanques = "Blanques"
        msg_negres = "Negres"
        rival1[indx].send(msg_blanques.encode())
        rival2[indx].send(msg_negres.encode())
        
        en_cua = en_cua - 2

    else:
        #
        self.sendLine("Please wait to be matched with another player");



#funció per acceptar clients, inicia el mètode conversa

def acceptar_clients(server):
    while True:
        client, addr = server.accept()
        clients.append(client)


        threading._start_new_thread(conversa_client, (client, addr))


# funció que rep i envia missatges amb el client
def conversa_client(client_connection, client_ip_addr):
    while True:
        client_msg  = client_connection.recv(4096).decode()
        if (client_msg == "Sortir"):
            break
        elif (client_msg == "Començar"):
            llista_cua.append(client_connection)
            en_cua = en_cua + 1
            matchMaking()
            while (client_connection not in rival1 and client_connection not in rival2):
                if (client_msg == "Sortir"):
                    llista_cua.pop(get_client_index(llista_cua, client_connection))
                    break
            while True:
                moviment  = client_connection.recv(4096).decode()
                if (moviment == "Sortir"):
                    #Eliminem els clients de les llistes
                    if (client_connection in rival1):
                        rival1[idx].close()
                        rival2[idx].close()
                        idx = get_client_index(rival1, client_connection)
                        del rival1[idx]
                        del rival2[idx]
                    elif (client_connection in rival2):
                        idx = get_client_index(rival2, client_connection)
                        rival1[idx].close()
                        rival2[idx].close()
                        del rival1[idx]
                        del rival2[idx]
                    break
                else:
                    if (client_connection in rival1):
                        rival2[get_client_index(rival1, client_connection)].send(moviment.encode())
                    elif (client_connection in rival2):
                        rival1[get_client_index(rival2, client_connection)].send(moviment.encode())

#mira només si el missatge és per fer un moviment o és una comanda per sortir de la partida.
#no comprova si el moviment és possible perquè això ja ho ha fet el client
def moviment_valid(missatge):
    valid = True
    if missatge[0] not in columnes:
        valid = False
    if missatge[1] not in files:
        valid = False
    if missatge[2] not in columnes:
        valid = False
    if missatge[3] not in files:
        valid = False
    return valid
#Retorna l'index de la llista on es troba el client
def get_client_index(client_list, client):
    idx = 0
    for x in client_list:
        if x == client:
            break
        idx = idx + 1

    return idx



