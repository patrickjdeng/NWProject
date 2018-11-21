''' Server : IN FROM BOTH R AND C'''
#!/usr/bin/env python
import socket
import subprocess

TYPE = 0
CODE = 1
DATA = 2
LENGTH = 3


def main():
    '''Server gives C list, gives R media to render'''
    control_port = 5300
    control_in_socket = create_listen_socket(control_port)  #wait for controller first
    render_port = 5500
    render_in_socket = create_listen_socket(render_port)
    server(control_in_socket, render_in_socket)
    control_in_socket.close()
    render_in_socket.close()


def create_listen_socket(port):
    '''create, make listen, return socket listening to any ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ''
    sock.bind((address, port))
    sock.listen(1)
    return sock


def server(control_in_socket, render_in_socket):
    '''get requests from controller and renderer'''
    control_conn, _ = control_in_socket.accept()
    render_conn, _ = render_in_socket.accept()
    message_type = 0
    while True:
        message_type = process_list_request_from(control_conn)
        if message_type =='3':
            break
        else:    
            message_type = process_file_request_from(render_conn)
            if message_type == '22':
                break


def process_list_request_from(conn):
    '''SERVER RECEIVE REQUEST FROM C, SENDS C LIST OR EXIT'''
    
    buff_size = 1024
    message_type = '0'
    while message_type != '1' and message_type != '3':
        message = conn.recv(buff_size).split(';')
        message_type = message[TYPE]   
    if message_type == '1':
        output = subprocess.check_output(['ls'])
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

# TODO: All of the stuff missing is in here
def process_file_request_from(conn):
    '''SERVER RECEIVE FILE REQUEST FROM R, SENDS R FILE'''
    buff_size = 1024
    message_type = '0'

    while message_type != '20' or message_type != '22':
        message = conn.recv(buff_size).split(';')
        message_type = message[TYPE]
    if message_type == '20':
        media_file = open()
        #TODO: Do we just look at the extensions to find these?
        file_not_found, file_is_text, file_is_video = True, True, True
        if file_not_found:
            out_message = '21;0' # status, media not found
            conn.send(out_message)
        elif file_is_text:
            out_message = '21;1' 
            conn.send(out_message)
        elif file_is_video:
            out_message = '21;2'
            conn.send(out_message)
    else:
        print 'Disconnected from Renderer'
    return message_type

main()
