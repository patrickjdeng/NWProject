''' Server : IN FROM BOTH R AND C'''
#!/usr/bin/env python
import socket
import subprocess
import os

TYPE = 0
CODE = 1
DATA = 2
LENGTH = 3
BUFFER_SIZE = 1024


def main():
    '''Server gives C list, gives R media to render'''
    control_port = 5300
    control_in_socket = create_listen_socket(control_port)  #wait for controller first
    render_port = 5500
    render_in_socket = create_listen_socket(render_port)
    server(control_in_socket, render_in_socket)



def server(control_in_socket, render_in_socket):
    '''get requests from controller and renderer'''
    os.chdir('server')
    control_conn, _ = control_in_socket.accept()
    render_conn, _ = render_in_socket.accept()
    while True:
        print "awaiting list request"
        message_type = process_list_request_from(control_conn)
        print "awaiting media request"
        message_type = process_file_request_from(render_conn)
        if message_type == '23':    #EXIT choice
            break

def create_listen_socket(port):
    '''create, make listen, return socket listening to any ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ''
    sock.bind((address, port))
    sock.listen(1)
    return sock


def file_is_image(name):
    '''Is the file an image'''
    dot_index = name.find('.')
    name = name[dot_index:]
    return '.jpeg' in name or \
        '.jpg' in name or \
            '.png' in name


def file_is_video(name):
    '''Is the file a video'''
    dot_index = name.find('.')
    name = name[dot_index:]
    return '.mp4' in name or \
        '.wmv' in name or \
            '.avi' in name


def file_not_found(filename):
    ''' If it was suddently deleted midway!'''
    ls_output = subprocess.check_output(['ls'])
    if ls_output == '':
        return True
    else:
        media_list = ls_output.split()
        for i in range(len(media_list)):
            media_list[i] = media_list[i].replace('\'', '').strip()
        return filename not in media_list



def process_file_request_from(conn):
    # R <-> S 1
    '''SERVER RECEIVE FILE REQUEST FROM R, SENDS R FILE INFO and FILE'''
    message_type = '0'
    while message_type != '20' and message_type != '23':
        message = conn.recv(BUFFER_SIZE).split(';')
        message_type = message[TYPE]
        if message_type != '':
            print message
    if message_type == '20':
        filename = message[DATA]
        if file_is_image(filename):
            out_message = '21;0'
            conn.send(out_message)
            send_file_when_ready(filename, conn)
        elif file_is_video(filename):
            out_message = '21;1'
            conn.send(out_message)
            send_file_when_ready(filename, conn)
        elif file_not_found(filename):
            out_message = '21;2' # status, media not found
            conn.send(out_message)
        else:
            out_message = '21;3'
            conn.send(out_message)
    else:
        print 'Disconnected from Renderer'
    return message_type


def process_list_request_from(conn):
    '''SERVER RECEIVE REQUEST FROM C, SENDS C LIST OR EXIT'''
    message_type = '0'
    while message_type != '1' and message_type != '3':
        message = conn.recv(BUFFER_SIZE).split(';')
        message_type = message[TYPE]
    if message_type == '1':
        ls_output = subprocess.check_output(['ls'])
        if ls_output == '':
            out_message = '0;2;' # status, none found
            conn.send(out_message)
        else:
            media_list = ls_output.split()
            out_message = '2;0;' + str(media_list)
            conn.send(out_message)
    elif message_type == '3':
        print 'Disconnected from controller'
    return message_type


def send_file_when_ready(filename, conn):
    '''Actually send the file bytes thru socket to R'''
    #wait for ok from renderer
    while True:
        in_message = conn.recv(BUFFER_SIZE).split(';')
        if in_message[TYPE] == '22':
            break
    media_file = open(filename).read()
    #SYNC R<-> S FILE WRITE
    conn.send(media_file)
    print "Done sending"
    return


main()
