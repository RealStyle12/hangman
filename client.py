import socket
import sys
import string

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

if __name__ == "__main__":
    sock = make_socket()
    sock.connect((HOST, PORT))  
    msg = sock.recv(18) # WELCOME TO HANGMAN
    print msg
    print sock.recv(1024)   # HANGMAN DRAWING
    keepGoing = True
    while keepGoing:
        guess = ""
        while True:
            guess = raw_input("Guess a letter: ").lower()
            if len(guess) > 1 or guess not in string.lowercase:
                print "Please guess a letter."
            else:
                break
        try:
            sock.sendall(guess)
        except socket.error:
            print "Client: Send failed."
            sys.exit()

        reply = sock.recv(1024)
        print reply
        if "You lose." in reply:
            play_again = raw_input("Play again? (y/n): ").lower()
            if 'n' in play_again:
                keepGoing = False
                print "Thanks for playing..."
            else:
                sock.sendall("1")
    sock.close()
