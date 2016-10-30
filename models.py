from pickle import *


# TODO Packet must be serializable
class Packet():
    packet_type = 3
    seq_num = 0
    window_size = 0
    ack_num = 0
    data = ''
    destination_address = ''
    destination_port = 0
    source_address = ''
    source_port = 0

    def __init__(self):
        self.packet_type = 3
        self.seq_num = 0
        self.window_size = 0
        self.ack_num = 0
        self.data = ''
        self.destination_adress = ''
        self.destination_port = 7777
        self.source_adress = ''
        self.source_port = ''


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
        return self.destination_adress

    def set_destination_address(self, destination_address):
        self.destination_address = destination_address

    def get_destination_port(self):
        return self.destination_port

    def set_destination_port(self, destination_port):
        self.destination_port = destination_port

    def get_source_address(self):
        return self.source_adress

    def set_source_adress(self, source_adress):
        self.source_address = source_adress

    def get_source_port(self):
        return self.source_port

    def set_source_port(self, source_port):
        self.source_port = source_port

    def __str__(self):
        info_string = '''Packet [packet type={}, seq num={},
         window size={}, ack num={}, data={},
        destination adress={}, destination port={},
        source address={}, source port={}]'''.format(self.packet_type, self.seq_num, self.window_size, self.ack_num, self.data, \
                                                     self.destination_adress, self.destination_port, self.source_address, self.source_port)
        return info_string
