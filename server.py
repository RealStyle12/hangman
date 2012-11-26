import socket
import sys
from thread import *
from hangman import Game

EOM = "::"
WAITING_FOR_CONN = 1
WAITING_FOR_MOVE = 2
WAITING_TO_PLAY_AGAIN = 3
WAITING_TO_START_GAME = 4
GAME_OVER = 5

def make_socket():
    HOST = sys.argv.pop() if len(sys.argv) == 3 else "127.0.0.1" 
    PORT = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error Code: ' + str(msg[0]) + ', Error Message: ' + msg[1]
        sys.exit()
    s.listen(1)
    return s

def read_msg(data):
    if len(data) == 0:
        return (None, data)

    EOM_index = data.find(EOM) 
    msg = data[0:EOM_index]
    data = data[EOM_index + len(EOM):]
    return (msg, data)

def init_game(conn):
    game = Game()
    conn.sendall("WELCOME TO HANGMAN" + EOM)
    conn.sendall(game.game_string() + EOM + str(game.gameover) + EOM)
    return game

def process_letter(game, letter):
    if game.already_guessed(letter):
        return "You've already guessed %r." % letter
    else:
        game.guess_letter(letter)
        return game.game_string(game.game_status())

def client_thread(conn):
    current_state = WAITING_TO_START_GAME
    data = ""
    while current_state is not GAME_OVER:
        if current_state is WAITING_TO_START_GAME:
            game = init_game(conn)
            current_state = WAITING_FOR_MOVE
        elif current_state is WAITING_FOR_MOVE:
            data += conn.recv(1024)
            letter, data = read_msg(data)
            reply = process_letter(game, letter)
            if game.gameover:
                current_state = WAITING_TO_PLAY_AGAIN
            conn.sendall(reply + EOM + str(game.gameover) + EOM)
        elif current_state is WAITING_TO_PLAY_AGAIN:
            data += conn.recv(1024)
            play_again, data = read_msg(data)
            if play_again == "play":
                current_state = WAITING_TO_START_GAME
            elif play_again == "quit":
                current_state = GAME_OVER
    conn.close()

if __name__ == "__main__":
    sock = make_socket()
    print "Server: Up and listening..."
    while True:
        clientsocket, addr = sock.accept()
        print "Connected with " + addr[0] + ":" + str(addr[1])
        start_new_thread(client_thread, (clientsocket,))
