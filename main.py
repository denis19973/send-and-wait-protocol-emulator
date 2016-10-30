import network_configuration
import udp_network
from network import *


def create_network_module():
    network_module = Network(network_configuration)
    network_module.print_configuration()
    network_module.run()


create_network_module()
