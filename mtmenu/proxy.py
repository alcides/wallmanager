import socket
from settings import *
import threading


class Proxy( threading.Thread ):
    APP_RUNNING = False

    def __init__(self):
        self.flag = True
        
        threading.Thread.__init__(self)
    
    
    def start_sockets(self):
        self.receive_sock = socket.socket( socket.AF_INET, # Internet
                              socket.SOCK_DGRAM ) # UDP
        self.receive_sock.bind( (UDP_IP, RECEIVING_PORT) )
        self.send_sock = socket.socket( socket.AF_INET, # Internet
                          socket.SOCK_DGRAM ) # UDP

    
    def run(self):
        print "PROXY RUNNING"
        try:
            self.execute()
            print "PROXY STOPPED"
        except:
            raise


    def execute(self):
        self.start_sockets()
        while self.flag:
            data= self.receive_sock.recv( 1024 ) # buffer size is 1024 bytes
            self.send_sock.sendto( data, (UDP_IP, SENDING_PORT_ONE) )
            if self.APP_RUNNING:
                self.send_sock.sendto( data, (UDP_IP, SENDING_PORT_TWO) )

proxy = Proxy()