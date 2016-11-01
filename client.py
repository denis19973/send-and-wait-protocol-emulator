from udp_network import *
from abc import ABCMeta, abstractmethod
import models
import client_configuration
import time


class Client(metaclass=ABCMeta):
    def __init__(self, mode):
        self.mode = mode

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def make_packet(self, packet_type):
        pass

    def initialize_udp_server(self, port):
        self.listen = UDP_network.create_server(port)

    def send_packet(self, packet):
        socket = UDP_network.create_socket()
        print(socket)
        UDP_network.send_packet(socket, packet, client_configuration.network_address, client_configuration.network_port)

    def set_configuration(self, network_address, network_port, transmitter_address, transmitter_port, \
                                  receiver_address, receiver_port, max_packet_to_send, window_size, max_timeout):
        client_configuration.network_address = network_address
        client_configuration.network_port = network_port
        client_configuration.transmitter_adress = transmitter_address
        client_configuration.transmitter_port = transmitter_port
        client_configuration.receiver_address = receiver_address
        client_configuration.receiver_port = receiver_port
        client_configuration.max_packet_to_send = max_packet_to_send
        client_configuration.window_size = window_size
        client_configuration.max_timeout = max_timeout

    def print_configuration(self):
        print('Mode: {}, Network Emulator Address: {} : {}'.format(self.mode, client_configuration.network_address, \
                                                                   client_configuration.network_port))


    # TODO add take input method


class Sender(Client):
    def __init__(self, mode):
        Client.__init__(self, mode)
        self.seq_num = 1
        self.packet_window = []

    def run(self):
        self.initialize_udp_server(client_configuration.transmitter_port)
        self.send_control_packet()
        self.packets_sent = 0

        while self.packets_sent < client_configuration.max_packets_to_sent:
            self.generate_window_and_send()
            self.waiting_for_acks = True
            self.set_time_for_acks()

            while len(self.packet_window) != 0:
                if not self.waiting_for_acks:
                    self.set_timer_for_acks()
                    print('Window status: {}'.format(len(self.packet_window)))

            self.packets_sent += client_configuration.window_size
            print('Sent packets {}'.format(self.packets_sent))


        self.send_of_transmission_packet()

    def send_control_packet(self):
        packet = self.make_packet(1)

        self.send_packet(packet)

        receiver_response = UDP_network.get_packet(self.listen)

        print(receiver_response)

    def send_end_of_transmission(self):
        packet = self.make_packet(4)
        self.send_packet(packet)

    def make_packet(self, packet_type):
        return models.Packet_Utilities.make_packet(client_configuration.receiver_address, \
                                                   client_configuration.receiver_port, \
                                                   client_configuration.transmitter_address, \
                                                   client_configuration.transmitter_port, \
                                                   packet_type, self.seq_num, \
                                                   self.seq_num, client_configuration.window_size)

    def generate_window_and_sent(self):
        for i in range(1, client_configuration.window_size):
            packet = self.make_packet(2)
            self.packet_window.append(packet)
            self.send_packet(packet)
            self.seq_num += 1

    def ack_timeout(self):
        self.stop_timer_and_receive()
        if len(self.packet_window) != 0:
            self.waiting_for_acks = True
            for i in range(1, len(self.packet_window)):
                packet = self.packet_window[i]
                self.send_packet(packet)

            self.set_timer_for_acks()

    def set_timer_for_acks(self):
        self.timer = True
        while self.timer:
            self.ack_timeout()
            time.sleep(client_configuration.max_timeout)

    def receive_acks(self):
        self.listen.settimeout(2)
        while len(self.packet_window) != 0 and self.waiting_for_acks:
            packet = UDP_network.get_packet(self.listen)

            if packet.get_packet_type() == 3:
                self.remove_packet_from_window(packet.get_ack_num())

    def remove_packet_from_window(self, ack_num):
        for i in range(0, len(self.packet_window)):
            if self.packet_window[i].get_ack_num == ack_num:
                self.packet_window.pop(i)

    def stop_timer_and_receive(self):
        self.timer = False
        self.waiting_for_acks = False










