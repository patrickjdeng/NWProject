'''RENDERER: IN FROM C, OUT TO S'''
#!/usr/bin/env python
import socket
import select
import numpy as np
import cv2 # must install externally!

TYPE = 0
CODE = 1
DATA = 2
BUFFER_SIZE = 1024
BUSY = False

def main():
    '''Renderer relays request from controller to S'''
    addr = '10.0.0.1'
    control_port = 5400
    control_in_socket = create_listen_socket(control_port)
    server_port = 5500
    server_socket = create_sender_socket(addr, server_port)
    renderer(control_in_socket, server_socket)
    server_socket.close()


def renderer(control_in_socket, server_out_socket):
    '''get filename from C, request from S, play from C'''
    control_conn, _ = control_in_socket.accept()
    while True:
        # C <-> R 1 ARE WE BUSY OR EXITING?
        msg_type = handle_status_or_exit_request(control_conn)
        if msg_type == '17':
            server_out_socket.send('23;0;') #dc from server
            break
        # C -> R 2 ACTUAL CHOICE
        filename = receive_choice_from_control(control_conn)
        media_type = get_file_from_server(filename, server_out_socket)
        confirm_with_controller(media_type, filename, control_conn)
        if media_type == '0':
            show_text(filename)
        elif media_type == '1':
            show_video(filename, control_conn) 


def confirm_with_controller(media_type, filename, control_conn):
    '''Send message to controller with type of media received'''
    out_message = '13' + ';' + media_type + ';' + filename
    control_conn.send(out_message)


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


def get_file_from_server(name, sock):
    '''RENDERER GET FILE FROM S'''
    # R <-> S 1
    out_message = '20;0;' + name
    sock.send(out_message)
    in_message = sock.recv(BUFFER_SIZE).split(';')
    while True:
        if in_message[TYPE] == '21':
            break
    media_type = in_message[CODE]
    sock.send('22;0;')  #send server ok to start sending
    #SYNC R<-> S FILE WRITE
    if media_type == '0' or media_type == '1':
        media_file = open(name, 'wb')
        file_chunk = sock.recv(BUFFER_SIZE)
        while True:
            media_file.write(file_chunk)
            if len(file_chunk) < BUFFER_SIZE:
                break
            file_chunk = sock.recv(BUFFER_SIZE)
        media_file.close()
    return media_type

def handle_status_or_exit_request(conn):
    '''tells C that RENDERER is busy or ready'''
    while True:
        message = conn.recv(BUFFER_SIZE).split(';')
        message_type = message[TYPE]
        if message_type == '10' or message_type == '17':
            break
    if message_type == '10':
        if BUSY:
            conn.send('11;1;')
        else:
            conn.send('11;0;')
    return message_type


def show_video(filename, sock):
    '''Render video, while getting commands from C'''
    cap = cv2.VideoCapture(filename)
    print 'ok'
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print 'last frame'
            while True:
                message = sock.recv(BUFFER_SIZE).split(';')
                if message[TYPE] == '14':
                    if message[CODE] == '2':
                        print 'rewind'
                        cap.set(2,0)
                        ret, frame = cap.read()
                        break
                    elif message[CODE] == '3':
                        break
            if message[CODE] == '3':
                print 'stopped'
                break
        code = play_frame(cap, frame, sock)
        if code == 3:
            break
    cap.release()
    cv2.destroyAllWindows()
    sock.send('16;0')

def play_frame(cap, frame, sock):
    '''Given frame, will listen for controller command and render the frame'''
    cv2.imshow('frame', frame)
    code = 0
    readable, _, _ = select.select([sock], [], [], 0)
    if sock in readable:
        message = sock.recv(BUFFER_SIZE).split(';')
        if message[TYPE] == '14':
            if message[CODE] == '1': #pause
                print 'pause'
                while True:
                    message = sock.recv(BUFFER_SIZE).split(';')
                    if message[TYPE] == '14':
                        if message[CODE] == '0':
                            print 'play'
                            break
                        elif message[CODE] == '2':
                            print 'rewind'
                            cap.set(2,0)
                        elif message[CODE] == '3':
                            break
            if message[CODE] == '2':
                print 'rewind'
                cap.set(2,0)
            if message[CODE] == '3':
                print 'stopped'
                code = 3
    cv2.waitKey(16)
    return code

def receive_choice_from_control(conn):
    '''RENDERER RECEIVE LIST CHOICE FROM C'''
    while True:
        message = conn.recv(BUFFER_SIZE).split(';')
        if message[TYPE] == '12' or message[TYPE] == '17':
            break
    if message[TYPE] == '12':
        return message[DATA]
    elif message[TYPE] == '17':
        return ''


def show_text(filename):
    #delete the file after finishing
    return

main()
