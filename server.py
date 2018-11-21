''' Server '''
#!/usr/bin/env python
import socket
import subprocess

TYPE = 0
CODE = 1
DATA = 2
LENGTH = 3


def server():
    '''Server gives C list, gives R media to render'''
    control_port = 5300
    control_socket = create_listen_socket(control_port)  #wait for controller first
    render_port = 5500
    render_socket = create_listen_socket(render_port)
    message_type = 0
    while message_type != '3':
        message_type = process_request_from(control_socket)
        if message_type !='3':    
            process_file_request_from(render_socket)
    control_socket.close()
    render_socket.close()


def create_listen_socket(port):
    '''create, make listen, return socket listening to any ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ''
    sock.bind((address, port))
    sock.listen(1)
    return sock


def process_request_from(sock):
    '''SERVER RECEIVE REQUEST FROM C, SENDS C LIST OR EXIT'''
    buff_size = 1024
    conn, _ = sock.accept()
    message_type = '0'
    while message_type != '1' and message_type != '3':
        message = conn.recv(buff_size).split(';')
        message_type = message[TYPE]   
    if message_type == '1':
        output = subprocess.check_output(['ls', '/home/patrick/CS4390/project'])
        if  output == '':
            out_message = '0;2;' # status, none found
            conn.send(out_message)
        else:
            media_list = output.split()
            out_message = '2;0;' + str(media_list) 
            conn.send(out_message)
    elif message_type == '3':
        print 'Disconnected from controller'
    return message_type

# TODO: stuff to do here
def process_file_request_from(sock):
    '''SERVER RECEIVE LIST REQUEST FROM R, SENDS R FILE'''
    buff_size = 1024
    message_type = '0'
    conn, _= sock.accept()

    while message_type != '1':
        message = conn.recv(buff_size).split(';')
        if message[TYPE] == '1':
            break
    media_file = subprocess.check_output(['ls', '-l', '/home/patrick/CS4390/project/videos'])
    file_not_found = True
    file_is_text = True
    file_is_video = True
    if file_not_found:
        out_message = '21;0' # status, media not found
        conn.send(out_message)
    elif file_is_text:
        out_message = '21;1' 
        conn.send(out_message)
    elif file_is_video:
        out_message = '21;2'


server()
