import client_configuration
from client import Client
from models import *
from udp_network import *


class Receiver(Client):
    def __init__(self, mode):
        Client.__init__(self, mode)
        self.current_seq_num = 0
        self.asked_packets = []

    def run(self):
        self.initialize_udp_server(client_configuration.receiver_port)
        self.wait_for_sot()

        keep_receiving = True

        total_packets = 0
        total_duplicate_acks = 0

        while keep_receiving:
            packet = UDP_network.get_packet(self.listen)

            pack_type = packet.get_packet_type()

            if pack_type == 4:
                keep_receiving = False
                break
            elif pack_type == 2:
                self.current_seq_num = packet.get_seq_num()
                ack_packet = self.make_packet(3)
                self.send_packet(ack_packet)
                if not self.find_if_packed_acked(packet.get_seq_num()):
                    total_packets += 1
                else:
                    total_duplicate_acks += 1

                self.asked_packets.append(packet)
                break

    def find_if_packed_acked(self, seq_num):
        for i in range(0, len(self.asked_packets)):
            if self.asked_packets[i].get_seq_num() == seq_num:
                return True

        return False

    def wait_for_sot(self):
        sot_packet = UDP_network.get_packet(self.listen)

        if sot_packet.get_packet_type() == 1:
            packet = self.make_packet(1)
            self.send_packet(packet)

        else:
            self.wait_for_sot()

    def make_packet(self, packet_type):
        return Packet_Utilities.make_packet(client_configuration.transmitter_address,
                                            client_configuration.transmitter_port, \
                                            client_configuration.receiver_address, client_configuration.receiver_port, \
                                            packet_type, self.current_seq_num, self.current_seq_num, \
                                            client_configuration.window_size)
