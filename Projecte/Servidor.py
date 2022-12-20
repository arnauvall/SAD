import socket
import threading
import time


files = ['1', '2', '3', '4', '5', '6', '7', '8']
columnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
client_name = " "
clients = []
llista_cua = []
clients_ids = []
en_cua = 0
rival1 = []
rival2 = []
rival_turn = []


def iniciar_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(acceptar_clients, (server, " "))



def matchMaking(self):
        #Find two players on a waiting list and make them play
        # Is there enough players in waiting queue
    if (en_cua >= 2):

        print (time.strftime("%H:%M") + " Matchmaking two players..")
            #Creating a shortlist of matched players at the moment
        rival1.append(llista_cua.pop(0))
        rival2.append(llista_cua.pop(0))
        rival_turn.append(True)
        indx = len(rival1)
        msg_blanques = "Blanques"
        msg_negres = "Negres"
        rival1[indx].send(msg_blanques.encode())
        rival2[indx].send(msg_negres.encode())
            #Maintaining numbers of players
        en_cua = en_cua - 2

    else:
            #Not enough players, you have to wait!
        self.sendLine("Please wait to be matched with another player");





def acceptar_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)


        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):

    while True:
        client_msg  = client_connection.recv(4096).decode()
        if (client_msg == "Sortir"):
            break
        elif (client_msg == "Començar"):
            msg_benvinguda = "Entres a la llista de matchmaking!"
            client_connection.send(msg_benvinguda.encode())
            llista_cua.append(client_connection)
            matchMaking()
            while (client_connection not in rival1 and client_connection not in rival2):
                if (client_msg == "Sortir"):
                    llista_cua.pop(get_client_index(llista_cua, client_connection))
                    break
            while True:
                moviment  = client_connection.recv(4096).decode()
                if (moviment == "Sortir"):
                    msg_sortir = "Fins la pròxima!"
                    client_connection.send(msg_sortir.encode())
                    client_connection.close()
                    break
                else:
                    if (client_connection in rival1):
                        rival2[get_client_index(rival1, client_connection)].send(moviment.encode())
                    elif (client_connection in rival2):
                        rival1[get_client_index(rival2, client_connection)].send(moviment.encode())
        else:
            msg_error = "Error"
            client_connection.send(msg_error.encode())


    while True:
        msg = client_connection.recv(4096).decode()
        if not msg: break
        if msg == "sortir": break

        client_msg = msg

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_ids[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_ids[idx]
    del clients[idx]
    server_msg = "BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()

def moviment_valid(missatge):
    #mirem només si el missatge és de
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
# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx



