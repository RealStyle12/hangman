EOM = "::"
class Messenger:
    def __init__(self, sock):
        self.data = ""
        self.sock = sock

    def read(self):
        if not EOM in self.data:
            self.data += self.sock.recv(1024)

        msg, self.data = self.data.split(EOM, 1)
        return msg

    def send(self, msg):
        self.sock.sendall(msg + EOM)
