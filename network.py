import socket

import network_configuration
from udp_network import *


class Network:
    # configuration for the network module

    def __init__(self, network_configuration):
        self.configuration = network_configuration

    def run(self):
        running_network = True

        total_packets = 0
        total_packets_dropped = 0
        total_packets_forwarded = 0

        sock = UDP_network.create_server(self.configuration.network_port)

        print('server running...')
        try:
            while running_network:
                packet = UDP_network.get_packet(sock)
                print(packet)
                total_packets += 1
                print('Total packets: {}'.format(total_packets))

                
        except KeyboardInterrupt:
            print('server stoped.')

    def print_configuration(self):
        print(
            'Drop rate: {}, Avarage Delay per Packet: {}, Sender: {}, Receiver: {}'.format(self.configuration.drop_rate, \
                                                                                           self.configuration.avarage_per_packet, \
                                                                                           self.configuration.sender, \
                                                                                           self.configuration.receiver))
