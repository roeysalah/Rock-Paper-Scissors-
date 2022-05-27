import pickle
import socket
from _thread import *
from game import Game
import sys

server = "" # put the ip address of the server (localhost)
port = 5555

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#seting connection by checking if port in use already
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for new connection...")

connected_set = set() # store the ip address of the clients connected to server
games={}
id_count = 0



def threaded_client(connection,player,game_id):
    """
    This function is responsible for the communication between the client and the server
    :param connection:
    :param player:
    :param game_id:
    :return:
    """
    global id_count # keep track how many players connected / games  are running
    connection.send(str.encode(str(player)))
    send_msg = ""
    while True :
        try:
            data_recv = connection.recv(4096).decode()
            if game_id in games:
                game=games[game_id]

                if not data_recv :
                    break
                # here we check if get msg for reset ,get or move
                else:
                    if data_recv == "Reset" :
                        game.reset_game()
                    elif data_recv != "Get":
                        game.player_move_update(player,data_recv)
                    send_msg = game
                    connection.sendall(pickle.dumps(send_msg))
            else:
                break

        except:
            break

    print("Connection lost !")
    try:
        del games[game_id]
        print("Closing Game {}".format(game_id))
    except:
        pass
    id_count-=1
    connection.close()







while True:
    connection, addr = s.accept()  # accept incoming connection
    print("Connected to :", addr)
    id_count+=1
    p_current = 0
    game_id = (id_count-1)//2
    if id_count % 2 == 1 :            # only one player connected ,waiting for second player !
        games[game_id] = Game(game_id)
        print("Creating New Game")
    # game ready to start - get two players !
    else:
        games[game_id].ready = True
        p_current = 1
    start_new_thread(threaded_client,(connection,p_current,game_id))

