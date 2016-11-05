import time
from abc import ABCMeta, abstractmethod

import client_configuration
import models
from udp_network import *


class Client(metaclass=ABCMeta):
    # Constructor. Initializes the client in a mode.
    def __init__(self, mode):
        self.configuration = client_configuration
        self.mode = mode

    # The main runner..where all the client running occurs (either sending or receiving).
    @abstractmethod
    def run(self):
        pass

    # Creates a packet from the configuration, sequence number, packet type and other details.
    @abstractmethod
    def make_packet(self, packet_type):
        pass

    # Initialize the Udp Server for listening.
    def initialize_udp_server(self, port):
        self.listen = UDP_network.create_server(port)

    # Send a packet to the network emulator.
    def send_packet(self, packet):
        socket = UDP_network.create_socket()
        UDP_network.send_packet(socket, packet, self.configuration.network_address, self.configuration.network_port)

    # Sets the client configuration.
    def set_configuration(self, network_address, network_port, transmitter_address, transmitter_port, \
                          receiver_address, receiver_port, max_packet_to_send, window_size, max_timeout):
        self.configuration.network_address = network_address
        self.configuration.network_port = network_port
        self.configuration.transmitter_adress = transmitter_address
        self.configuration.transmitter_port = transmitter_port
        self.configuration.receiver_address = receiver_address
        self.configuration.receiver_port = receiver_port
        self.configuration.max_packet_to_send = max_packet_to_send
        self.configuration.window_size = window_size
        self.configuration.max_timeout = max_timeout

    # Prints all configuration for the Client.
    def print_configuration(self):
        print('Mode: {0}, Network Emulator Address: {1} : {2}'.format(self.mode, self.configuration.network_address, \
                                                                      self.configuration.network_port))

    # Return client's current mode (sender or receiver).
    def get_mode(self):
        return self.mode

    # Set the client mode (sender or receiver).
    def set_mode(self, mode):
        self.mode = mode


class Sender(Client):
    # Create a client, whose sole purpose is to send (transmit) to the receiver.
    def __init__(self, mode):
        Client.__init__(self, mode)
        self.seq_num = 0
        self.packet_window = []

    def run(self):
        # initialize udp server
        self.initialize_udp_server(self.configuration.transmitter_port)
        # take control of the channel
        self.send_control_packet()
        # total packets sent so far
        self.packets_sent = 0

        # once, all ack's arrive, empty window, and move onto the next window
        while self.packets_sent < self.configuration.max_packets_to_sent:
            # generate packets for a window and send
            self.generate_window_and_send()
            # we are now waiting for ack's.
            self.waiting_for_acks = True
            # set timer and after it's over, check for ACK's.
            self.set_timer_for_acks()
            # wait for ack's for each packet
            while len(self.packet_window) != 0:
                # set a timer only if we are not already waiting..no point invoking it again and again
                if not self.waiting_for_acks:
                    # set timer and after it's over, check for ACK's.
                    self.set_timer_for_acks()
                    print('** Window status: {0}'.format(len(self.packet_window)))

            # windowSize number of more packets have been sent
            self.packets_sent += self.configuration.window_size
            print('Sent packets {0}'.format(self.packets_sent))
            print('Ramainings packets {0}'.format(self.configuration.window_size - self.packets_sent))
        # when all window packets sent, send EOT
        self.send_end_of_transmission()

    # Send the packet to take control of the communication channel.
    def send_control_packet(self):
        # create a SOT packet
        packet = self.make_packet(1)

        # send the packet
        self.send_packet(packet)

        # wait for SOT packet from receiver
        receiver_response = UDP_network.get_packet(self.listen)

        if receiver_response.get_packet_type() == 1:
            print('** packet SOT got from receiver!')

    # Send the packet to end the transmission.
    def send_end_of_transmission(self):
        # create an EOT packet.
        packet = self.make_packet(4)
        # send the packet
        self.send_packet(packet)
        print('** EOT sended')

    def make_packet(self, packet_type):
        return models.Packet_Utilities.make_packet(self.configuration.receiver_address, \
                                                   self.configuration.receiver_port, \
                                                   self.configuration.transmitter_address, \
                                                   self.configuration.transmitter_port, \
                                                   packet_type, self.seq_num, \
                                                   self.seq_num, self.configuration.window_size)

    # Generate packets for a full window.
    def generate_window_and_send(self):
        for i in range(1, self.configuration.window_size):
            # craft a data packet
            packet = self.make_packet(2)
            # add it to the window
            self.packet_window.append(packet)
            # send the packet
            self.send_packet(packet)
            print('** packet sended')
            # increment the sequence number
            self.seq_num += 1

    # Wait for ACK's for the packets sent in the window.
    def ack_timeout(self):
        self.stop_timer_and_receive()
        # if packet window isn't empty, send all those packets again, and wait for ack's.
        if len(self.packet_window) != 0:
            self.waiting_for_acks = True
            for i in range(1, len(self.packet_window)):
                packet = self.packet_window[i]
                self.send_packet(packet)

    # Set timer and wait for ACKs.
    def set_timer_for_acks(self):
        self.timer = True

        # call ackTimeout and check which packets have been ACK'ed.
        if self.timer:
            time.sleep(self.configuration.max_timeout)
            self.ack_timeout()

        self.receive_acks()

    # Wait for ACKs.
    def receive_acks(self):

        # can block for a maximum of 2 seconds

        try:
            self.listen.settimeout(10)

            # Scan while packet window size isn't 0. If 0, all packets have been ACK'ed.
            while len(self.packet_window) != 0 and self.waiting_for_acks:
                print('** waiting for ACK...')
                packet = UDP_network.get_packet(self.listen)

                # if an ACK received, log and remove from the window.
                if packet.get_packet_type() == 3:
                    print('** ACK got')
                    self.remove_packet_from_window(packet.ack_num)

        except socket.timeout:
            print('Timed out')

    # Checks all packets in the current window and removes the one whose acknowledgement number is
    # equal to the ACK number of the received packet.
    def remove_packet_from_window(self, ack_num):
        try:
            for i in range(len(self.packet_window)):
                if self.packet_window[i].ack_num == ack_num:
                    self.packet_window.pop(i)

        except IndexError:
            pass

    # Stop the timer.
    def stop_timer_and_receive(self):
        self.timer = False
        self.waiting_for_acks = False
