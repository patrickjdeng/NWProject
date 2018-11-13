'''Controller'''
#!/usr/bin/env python

import socket


def connect_to_renderer():
    """C connect to R"""

    server_ip = '10.0.0.1'
    server_port = 5300
    buffer_size = 1024
    message = "5;2;4"  # it'll request a list from the server
    #   prepare socket and connect
    r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_socket.connect((server_ip, server_port))
    #   send then wait for receive
    r_socket.send(message)
    response = r_socket.recv(buffer_size).split(';')
    print response[0]
    r_socket.close()

    


connect_to_renderer()
