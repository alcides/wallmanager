import socket
from settings import *
import threading


class Proxy( threading.Thread ):

    def __init__(self):
        self.flag = False
        threading.Thread.__init__(self)
    
    
    def start_sockets(self):
        self.receive_sock = socket.socket( socket.AF_INET, # Internet
                              socket.SOCK_DGRAM ) # UDP
        self.receive_sock.bind( (UDP_IP, RECEIVING_PORT) )
        self.send_sock = socket.socket( socket.AF_INET, # Internet
                          socket.SOCK_DGRAM ) # UDP

    
    def run(self):
        try:
            self.execute()
        except:
            pass


    def execute(self):
        self.start_sockets()
        while self.flag:
            data, addr = self.receive_sock.recvfrom( 1024 ) # buffer size is 1024 bytes
            print data
            self.send_sock.sendto( data, (UDP_IP, SENDING_PORT_ONE) )
            self.send_sock.sendto( data, (UDP_IP, SENDING_PORT_TWO) )

