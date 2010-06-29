import socket
from config import PROXY_UDP_IP, PROXY_RECEIVING_PORT, PROXY_SENDING_PORT_ONE, PROXY_SENDING_PORT_TWO
import threading
from mtmenu.application_running import is_app_running
from mtmenu import logger


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
        logger.info("PROXY RUNNING")
        try:
            self.execute()
            logger.info("PROXY STOPPED")
        except Exception, e: #Pokemon
            if logger:
                logger.error("EXCEPTION ON PROXY:\n%s" % e)
            except:
                print "Exception on Proxy:", e


    def execute(self):
        self.start_sockets()
        logger.info("PROXY SOCKETS STARTED")
        while self.flag:
            data = self.receive_sock.recv( 30 * 1024 ) # buffer size is 30 * 1024 bytes
            self.send_sock.sendto( data, (PROXY_UDP_IP, PROXY_SENDING_PORT_ONE) )
            if is_app_running():
                self.send_sock.sendto( data, (PROXY_UDP_IP, PROXY_SENDING_PORT_TWO) )

proxy = Proxy()
