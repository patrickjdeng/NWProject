from socket import *


def request_list():
    buffer_size = 1024
    message = ""  # it'll request a list from the server
    server_port = 8080

    #   prepare socket and connect
    controller_socket = socket(AF_INET, SOCK_STREAM)
    controller_socket.connect(('localhost', server_port))  # TODO: Discuss port

    #   send then wait for receive
    controller_socket.send(message)
    server_data = controller_socket.recv(buffer_size)
    controller_socket.close()
