'''Controller'''
#!/usr/bin/env python

import socket


def main():
    ''' entire renderer operation'''
    addr = '10.0.0.1'
    port = 5300
    r_out_socket = create_sender_socket(addr, port)
    message = "5;2;4"  # it'll request a list from the server
    r_out_socket.send(message)
   
    buffer_size = 1024
    response = r_out_socket.recv(buffer_size).split(';')
    print response[0]
    r_out_socket.close()


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
