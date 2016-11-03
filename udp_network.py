import pickle
import socket

from models import Packet


class UDP_network:
    # Creates a UDP Socket that listens on a specified port.
    def create_server(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('',port))
        return sock
    # # Creates a UDP Socket that listens on a specified port.
    def create_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Read a Packet from the UDP socket.
    def get_packet(socket):
        byte_data = socket.recv(1024)
        packet = pickle.loads(byte_data)
        return packet

    # Send a Packet from the UDP socket to destination specified inside the Packet.
    def send_packet(socket, packet, destination_address=None, destination_port=None):
        if destination_address != None:
            byte_packet = pickle.dumps(packet)
            socket.sendto(byte_packet, (destination_address, destination_port))
        else:
            byte_packet = pickle.dumps(packet)
            print('work from packet!!! ')
            socket.sendto(byte_packet, (packet.get_destination_address(), packet.get_destination_port()))
