import client_configuration
from client import Client
from models import *
from udp_network import *


class Receiver(Client):
    # Create a client whose sole purpose is to receive from the sender (transmitter).
    def __init__(self, mode):
        Client.__init__(self, mode)
        self.current_seq_num = 0
        self.asked_packets = []

    def run(self):
        # initialize udp server
        self.initialize_udp_server(self.configuration.receiver_port)
        # listen for SOT
        self.wait_for_sot()
        # Receive until this is true.
        self.keep_receiving = True

        total_packets = 0
        total_duplicate_acks = 0

        while self.keep_receiving:
            # scan each packet
            packet = UDP_network.get_packet(self.listen)
            print(packet)
            pack_type = packet.get_packet_type()

            if pack_type == 4:
                # listen for EOT
                print('Total packets received: {0}, Total duplicate ACKs: {1}'.format(total_packets, total_duplicate_acks))
                self.keep_receiving = False
                break
            elif pack_type == 2:
                # update current sequence number
                self.current_seq_num = packet.get_seq_num()

                # craft and send ACK packet
                ack_packet = self.make_packet(3)
                print('creating ack ...')
                print(ack_packet)
                self.send_packet(ack_packet)
                print('ack send')
                # if packet hasn't been ACK'ed before.
                if not self.find_if_packed_acked(packet.get_seq_num()):
                    total_packets += 1
                else:
                    # ACKing again - earlier ACK probably got lost
                    total_duplicate_acks += 1

                # add to list of ack'ed packets
                self.asked_packets.append(packet)
                break
    # Find if the current packet has ever been ack'ed before.
    def find_if_packed_acked(self, seq_num):
        for i in range(0, len(self.asked_packets)):
            if self.asked_packets[i].get_seq_num() == seq_num:
                return True

        return False

    # Waits for Sender to send a SOT.
    def wait_for_sot(self):
        sot_packet = UDP_network.get_packet(self.listen)



        if sot_packet.get_packet_type() == 1:

            # send SOT back to signify receive.
            print('SOT from sender got')
            packet = self.make_packet(1)
            self.send_packet(packet)

        else:

            # malicious packet - continue.
            self.wait_for_sot()

    def make_packet(self, packet_type):
        return Packet_Utilities.make_packet(self.configuration.transmitter_address,
                                            self.configuration.transmitter_port, \
                                            self.configuration.receiver_address, self.configuration.receiver_port, \
                                            packet_type, self.current_seq_num, self.current_seq_num, \
                                            self.configuration.window_size)
