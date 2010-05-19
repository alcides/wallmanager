import socket
from config import PROXY_UDP_IP, PROXY_RECEIVING_PORT, PROXY_SENDING_PORT_ONE, PROXY_SENDING_PORT_TWO
import threading
from mtmenu.application_running import is_app_running


class Proxy( threading.Thread ):

    def __init__(self):
        self.flag = True
        
        threading.Thread.__init__(self)
    
    
    def start_sockets(self):
        self.receive_sock = socket.socket( socket.AF_INET, # Internet
                              socket.SOCK_DGRAM ) # UDP
        self.receive_sock.bind((PROXY_UDP_IP, PROXY_RECEIVING_PORT))
        self.send_sock = socket.socket( socket.AF_INET, # Internet
                          socket.SOCK_DGRAM ) # UDP

    
    def run(self):
        print "PROXY RUNNING"
        try:
            self.execute()
            print "PROXY STOPPED"
        except Exception, e: #Pokemon
            print "EXCEPTION ON PROXY"
            print e 


    def execute(self):
        self.start_sockets()
        print "PROXY SOCKETS STARTED"
        while self.flag:
            data= self.receive_sock.recv( 1024 ) # buffer size is 1024 bytes
            self.send_sock.sendto( data, (PROXY_UDP_IP, PROXY_SENDING_PORT_ONE) )
            if is_app_running():
                self.send_sock.sendto( data, (PROXY_UDP_IP, PROXY_SENDING_PORT_TWO) )

proxy = Proxy()
