import network_configuration
import socket

class Network:
    # configuration for the network module
    configuration = network_configuration

    def Network(self, configuration_file):
        self.configuration = configuration_file

    def run(self):
        running_network = true

        total_packets = 0
        total_packets_dropped = 0
        total_packets_forwarded = 0




