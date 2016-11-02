import network_configuration
import udp_network
from client import *
from network import *
from receiver import *

print(
    'Welcome to the Send and Wait Protocol Simulator (Python version)\nYou can be one of the following: \n1)Enter 1 to be a Sender\n2)Enter 2 to be a receiver\n3)Enter 3 to be a Network Emulator ')
mode = input('Please enter mode: ')


def create_network_module():
    network_module = Network(network_configuration)
    network_module.print_configuration()
    print('You are now Network Emulator!')
    network_module.run()


try:
    if int(mode) == 1:
        sender = Sender(1)
        sender.print_configuration()
        print('You are now sender!')
        sender.run()
    elif int(mode) == 2:
        receiver = Receiver(2)
        receiver.print_configuration()
        print('You are now receiver!')
        receiver.run()
    elif int(mode) == 3:
        create_network_module()
except KeyboardInterrupt:
    print('server stopped.')
