import pickle
import random
import socket
import time

from udp_network import *


class Network:
    # configuration for the network module
    def __init__(self, network_configuration):
        self.configuration = network_configuration

    # The main runner..where all the main Network emulation occurs!
    def run(self):
        # run switch for the loop
        running_network = True

        # stats
        total_packets = 0
        total_packets_dropped = 0
        total_packets_forwarded = 0

        sock = UDP_network.create_server(self.configuration.network_port)

        print('server running...')
        try:
            # run forever - basically
            while running_network:
                packet = UDP_network.get_packet(sock)
                print(packet)
                total_packets += 1
                print('Total packets: {0}'.format(total_packets))

                # if it's a control packet, let it go through.
                if packet.get_packet_type() == 1 or packet.get_packet_type() == 4:
                    print(packet.get_destination_address(), packet.get_destination_port())
                    UDP_network.send_packet(sock, packet, packet.get_destination_address(),
                                            packet.get_destination_port())
                    total_packets_forwarded += 1

                else:

                    # if packet drop rate is lower than the threshold, drop it.
                    if self.get_drop_rate_threshold() <= self.configuration.drop_rate:
                        total_packets_dropped += 1
                        print('** packet dropped!')
                    else:

                        # if packet drop rate is greater than the threshold, let it go through.
                        time.sleep(self.configuration.average_per_packet)
                        UDP_network.send_packet(sock, packet)
                        total_packets_forwarded += 1


        except KeyboardInterrupt:
            print('server stoped.')

    # Returns a randomly calculated drop rate threshold. If the packet drop rate specified by the
    # * user is lower than or equal to this number, it is dropped.
    def get_drop_rate_threshold(self):
        thresold = random.randint(0, ((100 - 1) + 1) + 1)
        return thresold

    #  Prints all configuration for the Network Module.
    def print_configuration(self):
        print(
            'Drop rate: {0}, Avarage Delay per Packet: {1}, Sender: {2}, Receiver: {3}'.format(
                self.configuration.drop_rate, \
                self.configuration.average_per_packet, \
                (
                    self.configuration.sender_address,
                    self.configuration.sender_port), \
                (
                    self.configuration.receiver_address, \
                    self.configuration.receiver_port)))
