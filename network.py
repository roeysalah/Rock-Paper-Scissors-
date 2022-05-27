import socket
import pickle
class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "" # put the ip address of the server (localhost)
        self.port = 5555
        self.addr = (self.server,self.port)
        self.p = self.connect()

    def get_p(self):
        """
        This function get the player number from the server
        :return:
        """
        return self.p

    def connect(self):

        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send_message(self,data):
        """
        This function send the message to the server
        :param data:
        :return:
        """
        try:
            self.client.send(str.encode(data)) # send data to server
            return pickle.loads(self.client.recv(2048*2)) # receive object
        except socket.error as e :
            print(e)