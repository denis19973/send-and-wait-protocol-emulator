from models import *
from udp_network import *

pack = Packet()
pack.set_packet_type(2)
pack.set_destination_address('127.0.0.2')
pack.set_destination_port(8889)

socketok = UDP_network.create_socket()

UDP_network.send_packet(socketok, pack, 'localhost', 8888)