''' Server '''
#!/usr/bin/env python

import socket

def main():
    '''Server gives C list, gives R media to render'''
    c_port = 5500
    r_port = 5600
    address = '10.0.0.1'
    c_in_socket = create_listen_socket(c_port)  #wait for controller first
    c_response = handle_controller_request(c_in_socket)
    r_in_socket = create_listen_socket(r_port)

    
def create_sender_socket(addr, port):
    '''create, connect, return socket sending to certain ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    return sock


def create_listen_socket(port):
    '''create, make listen, return socket listening to any ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ''
    sock.bind((address, port))
    sock.listen(1)
    return sock


def handle_controller_request(in_socket):
    buffer_size = 1024
    media_list = []
    while True:
        print 'Waiting for request'
        message = in_socket.recv(buffer_size).split(';') # receive list request
        if message[0] == '1':
            media_list = 
        else:
            continue
    # get response and return  
    return media_list


def handle_renderer_request(in_socket, out_socket):
    in_socket # receive list request
    out_socket # send list back
    message = # get response and return  
    return messagex


main()