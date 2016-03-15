import socket
import sys
from thread import *
from Hangman import Game
from messenger import Messenger

WAITING_FOR_CONN = 1
WAITING_FOR_MOVE = 2
WAITING_TO_PLAY_AGAIN = 3
WAITING_TO_START_GAME = 4
GAME_OVER = 5

def make_socket():
    HOST = sys.argv.pop() if len(sys.argv) == 2 else "127.0.0.1" 
    PORT = 8888
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        Socket.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error Code: ' + str(msg[0]) \
                + ', Error Message: ' + msg[1]
        sys.exit()
    Socket.listen(1)
    return Socket

def init_game(messenger):
    game = Game()
    messenger.send("WELCOME TO HANGMAN")
    messenger.send(str(game))
    messenger.send(str(game.gameover))
    return game

def client_thread(conn):
    current_state = WAITING_TO_START_GAME
    messenger = Messenger(conn)
    while current_state is not GAME_OVER:
        if current_state is WAITING_TO_START_GAME:
            game = init_game(messenger)
            current_state = WAITING_FOR_MOVE
        elif current_state is WAITING_FOR_MOVE:
            messenger.send( str (game.incorrect + game.correct) );
            letter = messenger.read()
            if game.already_guessed(letter):
                reply = "You've already guessed %r." % letter
            else:
                game.guess_letter(letter)
                reply = str(game)

            if game.gameover:
                current_state = WAITING_TO_PLAY_AGAIN
            messenger.send(reply)
            messenger.send(str(game.gameover))
        elif current_state is WAITING_TO_PLAY_AGAIN:
            play_again = messenger.read()
            if play_again == "play":
                current_state = WAITING_TO_START_GAME
            elif play_again == "quit":
                current_state = GAME_OVER

    conn.close()

if __name__ == "__main__":
    sock = make_socket()
    print "Server: Up and listening..."
    while True:
        clientsocket, Connections = sock.accept()
        print "Connected with " + Connections[0] + ":" + str(Connections[1])
        start_new_thread(client_thread, (clientsocket,))
