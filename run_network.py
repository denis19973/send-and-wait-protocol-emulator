import network_configuration
from network import *

def create_network_module():
    network_module = Network(network_configuration)
    # print loaded configuration
    network_module.print_configuration()
    print('You are now Network Emulator!')
    # start
    network_module.run()

create_network_module()


