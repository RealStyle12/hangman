import socket
import sys
from thread import *
from hangman import Game

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

def client_thread(conn):
    keepGoing = True
    game = Game()
    conn.sendall("WELCOME TO HANGMAN")
    while keepGoing:
        conn.sendall(game.game_string())
        while not game.gameover:
            data = conn.recv(1)
            if not data:
                break
            reply = ""
            if game.already_guessed(data):
                reply += "You've already guessed %r." % data
            else:
                game.guess_letter(data)
                reply += game.game_string()
            conn.sendall(reply)
        data = conn.recv(1)
        if data == "1":
            game = Game()
        else:
            break
    conn.close()
    #print "client closed."

if __name__ == "__main__":
    sock = make_socket()
    print "Server: Up and listening..."
    while True:
        clientsocket, addr = sock.accept()
        print "Connected with " + addr[0] + ":" + str(addr[1])
        start_new_thread(client_thread, (clientsocket,))
