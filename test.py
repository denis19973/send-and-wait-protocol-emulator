from udp_network import *
import socket
import pickle
from models import *


a = Packet()
a.set_data(['heellppp', 1234524])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_network.send_packet(sock, a, '127.0.0.1', 8888)
