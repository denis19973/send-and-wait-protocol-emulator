import socket
from models import Packet

class UDP_network:
    def create_server(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind('', port)
        sock.listen(10)
        return sock

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    
    def get_packet(self, socket):
        data_bytes = socket.recv(1024)
        return data_bytes

    def send_packet(self, socket, packet, destination_adress='', destination_port=0):
        if destination_adress != '':
            socket.sendto(packet, (destination_adress, destination_port))
        else:
            socket.sendto(packet, (packet.get_destination_adress, packet.get_destination_port))

