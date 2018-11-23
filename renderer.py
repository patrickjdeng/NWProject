'''RENDERER: IN FROM C, OUT TO S'''
#!/usr/bin/env python
import socket
import numpy
import cv2 as cv # must install externally!

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

# TODO: HOW TO ACTUALLY PLAY THE VIDEO/TEXT ONCE WE HAVE IT?
def renderer(control_in_socket, server_out_socket):
    '''get filename from C, request from S, play from C'''
    control_conn, _ = control_in_socket.accept()
    while True:
        # C <-> R 1 ARE WE BUSY OR EXITING?
        msg_type = handle_status_or_exit_request(control_conn)
        if msg_type == '16':
            server_out_socket.send('23;0;') #dc from server
            break
        # C -> R 2 ACTUAL CHOICE
        filename = receive_choice_from_control(control_conn)
        media_type = get_file_from_server(filename, server_out_socket)
        confirm_with_controller(media_type, filename, control_conn)
        if media_type == '0':
            show_text(filename)
        elif media_type == '1':
            # play_video(filename) # still a WIP, dont wanna break things yet
            return
        # func(media_file)


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
        if message_type == '10' or message_type == '16':
            break
    if message_type == '10':
        if BUSY:
            conn.send('11;1;')
        else:
            conn.send('11;0;')
    return message_type

#TODO: Literally from stackoverflow
def play_video(filename):
    '''Render video, while getting commands from C'''
    capture  = cv.VideoCapture(0)
    media_file = open(filename)
    num_frames = int(  cv.GetCaptureProperty(media_file, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty(media_file, cv.CV_CAP_PROP_FPS )
    frame_delay = int( 1/fps * 1000/1 )

    for f in xrange( num_frames ):
        frame_image = cv.QueryFrame(media_file)
        cv.ShowImage( "My Video Window",  frame_image )
        cv.WaitKey(frame_delay)

    # When playing is done, delete the window
    #  NOTE: this step is not strictly necessary,
    #         when the script terminates it will close all windows it owns anyways
    cv.destroy_window( "My Video Window" )
    BUSY = False


def receive_choice_from_control(conn):
    '''RENDERER RECEIVE LIST CHOICE FROM C'''
    while True:
        message = conn.recv(BUFFER_SIZE).split(';')
        if message[TYPE] == '12' or message[TYPE] == '16':
            break
    if message[TYPE] == '12':
        return message[DATA]
    elif message[TYPE] == '16':
        return ''

#TODO: placeholder till we figure out how to do this
def receive_playback_command_from(sock):
    '''DO CERTAIN VIDEO THINGS BASED ON COMMAND FROM C'''
    #delete the file after finishing
    return 0

#TODO: hmm txt... discussion?
def show_text(filename):
    #delete the file after finishing
    return

main()