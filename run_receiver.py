from receiver import *

try:
    receiver = Receiver(2)
    print('You are now Receiver!')
    receiver.print_configuration()

    # start
    print('Receiver running...')
    receiver.run()
except KeyboardInterrupt:
    print('Receiver stopped')
