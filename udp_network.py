import socket
import pickle
from models import Packet


class UDP_network:
    def create_server(port=8888):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        return sock


    def get_packet(socket):
        byte_data = socket.recv(1024)
        packet = pickle.loads(byte_data)
        return packet

    def send_packet(socket, data, destination_adress='', destination_port=0):
        if destination_adress != '':
            packet = pickle.dumps(data)
            print(packet)
            socket.sendto(packet, (destination_adress, destination_port))
        else:
            socket.sendto(packet, (packet.get_destination_adress, packet.get_destination_port))

