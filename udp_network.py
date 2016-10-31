import socket
import pickle
from models import Packet


class UDP_network:
    def create_server(port=8555):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        return sock

    def create_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def get_packet(socket):
        byte_data = socket.recv(1024)
        packet = pickle.loads(byte_data)
        return packet

    def send_packet(socket, packet, destination_address='', destination_port=7777):

        print(destination_address, destination_port)
        if destination_address != '':
            packet.set_destination_address(destination_address)
            packet.set_destination_port(destination_port)
            byte_packet = pickle.dumps(packet)
            socket.sendto(byte_packet, (destination_address, destination_port))
        else:
            byte_packet = pickle.dumps(packet)
            socket.sendto(byte_packet, (packet.get_destination_address(), packet.get_destination_port()))

