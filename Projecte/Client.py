import socket
import threading


client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080



def connectar_servidor():
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))

        threading._start_new_thread(rebre_msg, (client, "m"))
    except Exception as e:
        print(title="ERROR!!!", message="No ens podem connectar al host: " + HOST_ADDR + " al port: " + str(HOST_PORT));


def rebre_msg(sck):

    msg = sck.recv(4096).decode()      
    return msg



def enviar_msg(msg):
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "Sortir":
        client.close()
    print("S'ha tancat la conexió")

