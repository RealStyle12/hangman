import socket
import sys
import string
import pdb

HOST = sys.argv.pop() if len(sys.argv) == 3 else "127.0.0.1" 
PORT = 8888

def make_socket():
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print "Client: Failed to create socket. Error code: " + str(msg[0]) + ", Error message: " + msg[1]
        sys.exit()
    #print "Client: Socket created."
    return c

WAITING_FOR_BOARD = 0
WAITING_FOR_GAME_STATUS = 1
WAITING_FOR_USER_INPUT = 2
WAITING_TO_PLAY_AGAIN = 3
WAITING_FOR_WELCOME = 4
GAME_OVER = 5

EOM = "::"

def read_msg(data):
    if len(data) == 0:
        return (None, data)

    EOM_index = data.find(EOM)
    msg = data[0:EOM_index]
    data = data[EOM_index + len(EOM):]
    return (msg, data)

if __name__ == "__main__":
    sock = make_socket()
    sock.connect((HOST, PORT))

    current_state = WAITING_FOR_WELCOME
    data = ""
    while current_state is not GAME_OVER:
        if current_state is WAITING_FOR_WELCOME:
            data += sock.recv(1024)
            welcome, data = read_msg(data)
            print welcome
            current_state = WAITING_FOR_BOARD
        elif current_state is WAITING_FOR_BOARD:
            data += sock.recv(1024)
            board, data = read_msg(data)
            print board
            current_state = WAITING_FOR_GAME_STATUS
        elif current_state is WAITING_FOR_GAME_STATUS:
            if not data:
                data += sock.recv(1024) # blocking issues??
            gameover, data = read_msg(data)
            if gameover == "True":
                current_state = WAITING_TO_PLAY_AGAIN
            elif gameover == "False":
                current_state = WAITING_FOR_USER_INPUT
        elif current_state is WAITING_FOR_USER_INPUT:
            guess = raw_input("Guess a letter: ").lower()
            if len(guess) > 1 or guess not in string.lowercase:
                print "Please guess a letter."
            else:
                sock.sendall(guess + EOM)
                current_state = WAITING_FOR_BOARD
        elif current_state is WAITING_TO_PLAY_AGAIN:
            play_again = raw_input("Play again? (y/n): ").lower()
            if "y" in play_again:
                current_state = WAITING_FOR_WELCOME
                sock.sendall("play" + EOM)
            else:
                current_state = GAME_OVER
                sock.sendall("quit" + EOM)
                print "Thanks for playing"
    sock.close()
