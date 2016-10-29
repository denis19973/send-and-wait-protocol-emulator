import socket

class UDP_network:
    def create_server(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind('', port)
        sock.listen(10)
        return sock

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # TODO add functions and model packet
    def get_packet(self, socket):
        data_bytes = socket.recv(1024)
        input_stream = data_bytes.decode('utf-8')
        return input_stream

    def send_packet(selfself, socket, packet):
        pass

