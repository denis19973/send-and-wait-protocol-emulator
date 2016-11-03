from client import *

try:
    a = Sender(1)
    print('You are now Sender')
    a.print_configuration()
    # start
    print('Sender running...')
    a.run()
except KeyboardInterrupt:
    print('Sender stopped')