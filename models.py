from pickle import *

class Packet():
    def __init__(self):
        self.packet_type = 0
        self.seq_num = 0
        self.window_size = 0
        self.ack_num = 0
        self.data =''
        self.destination_address = ''
        self.destination_port = 0
        self.source_address = ''
        self.source_port = 0

    def get_packet_type(self):
        return self.packet_type

    def set_packet_type(self, packet_type):
        self.packet_type = packet_type

    def get_seq_num(self):
        return self.packet_type

    def set_seq_num(self, seq_num):
        self.seq_num = seq_num

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size

    def get_ack_num(self):
        return self.ack_num

    def set_ack_num(self, ack_num):
        self.ack_num = ack_num

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_destination_address(self):
        return self.destination_address

    def set_destination_address(self, destination_address):
        self.destination_address = destination_address

    def get_destination_port(self):
        return self.destination_port

    def set_destination_port(self, destination_port):
        self.destination_port = destination_port

    def get_source_address(self):
        return self.source_address

    def set_source_address(self, source_address):
        self.source_address = source_address

    def get_source_port(self):
        return self.source_port

    def set_source_port(self, source_port):
        self.source_port = source_port

    def __str__(self):
        info_string = '''Packet [packet type={0}, seq num={1},
         window size={2}, ack num={3}, data={4},
        destination address={5}, destination port={6},
        source address={7}, source port={8}]'''.format(self.packet_type, self.seq_num, self.window_size, self.ack_num,
                                                     self.data, \
                                                     self.destination_address, self.destination_port,
                                                     self.source_address, self.source_port)
        return info_string


class Packet_Utilities():
    def make_packet(destination_address, destination_port, source_address, source_port, packet_type, \
                    seq_num, ack_num, window_size):
        packet = Packet()

        if packet_type == 1:
            packet.set_data('SOT')
        elif packet_type == 2:
            packet.set_data('packet number: {0}'.format(seq_num))
        elif packet_type == 3:
            packet.set_data('ack num {0}'.format(ack_num))
        elif packet_type == 4:
            packet.set_data('EOT')

        packet.set_destination_address(destination_address)
        packet.set_destination_port(destination_port)
        packet.set_source_address(source_address)
        packet.set_source_port(source_port)
        packet.set_packet_type(packet_type)
        packet.set_seq_num(seq_num)
        packet.set_ack_num(ack_num)
        packet.set_window_size(window_size)

        return packet
