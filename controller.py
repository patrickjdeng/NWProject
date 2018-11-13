from socket import *


def request_list():
    buffer_size = 1024
    message = "5,2,4"  # it'll request a list from the server
    server_port = 16000
    #   prepare socket and connect
    controller_socket = socket(AF_INET, SOCK_STREAM)
    controller_socket.connect(('127.0.0.1', 12000))  # TODO: Discuss port

    #   send then wait for receive
    controller_socket.send(message)
    response = controller_socket.recv(buffer_size).split()
    print response[0]
    controller_socket.close()


request_list()
