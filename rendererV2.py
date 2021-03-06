'''
renderer.py
Zack Oldham
11/04/2018
The renderer broadcasts its presence and waits for a connection from a controller.
When C connects, it sends a request to r_er to get a file
from the server which the r_er will then display as commanded
by the controller.
'''
#!/usr/bin/env python


import socket


def main():
    """ Run the entire renderer! Both connections!"""
    while True:
        r_ip = ''
        c_port = 5300
        buffer_size = 1024
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c_socket.bind((r_ip, c_port))
        c_socket.listen(1)
        print "waiting for connection..."
        c_socket, c_address = c_socket.accept()
        print "connection successful"
        print c_address
        #current status message from the controller
        message = c_socket.recv(buffer_size).split(';') 
        # recv_message = [type, code, data] --> data: None or [serverAddress, fileName]

        if message[0] == '5':     #so far so good, controller is idle so communicate accordingly
            send_message = '6;0;None'
            c_socket.send(send_message)
            receive_request(c_socket, c_port, buffer_size)
        else: #error occurred, terminate connection
            print "invalid controller message"
            send_message = '10;1;None'
            c_socket.close()
            return


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

def receive_request(c_socket, renderer_port, buffer_size):
    '''R receives filename from C'''
    return

'''

message = ['3', '', '']
while message[0] != 10:
    #File to Display message from controller
    message = c_socket.recv(buffer_size).split(';')
    s_port = 5400
    if message[0] == 3:
        if message[2][0] == 'None' or message[2][1] == 'None': # TODO: what is this?
            print "invalid file request: must provide server Address and file name"
            continue
        else:
            file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            file_socket.connect((message[2][0], s_port))
            send_message = [11, 'None', message[2][1]]
            file_socket.send(send_message)
            message = file_socket.recv(1024)

            if message[0] != 12:
                print "invalid response from server, try again"
                continue
            elif message[1] == 0:
                print "file not found"
                continue
            elif message[1] == 1:
                # display text file and process commands from controller as they arrive
                continue
                # at some point controller is through and issues termination message causing inner loop to end                    
            else:
                # display video file and process commands from controller as they arrive
                continue
                # at some point controller is through and issues termination message causing inner loop to end
    else:
        print "invalid file request, try again"
        continue
'''

def request_media(out_socket, in_socket):
    ''' send request for media to server, return -1 if fail, or video file if success '''
    return

main()