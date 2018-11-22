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
    control_in_socket.close()
    server_socket.close()


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

# TODO: what to do after we have media file and type!
def renderer(control_in_socket, server_out_socket):
    '''get filename from C, request from S, play from C'''
    # TODO: break when controller sends disconnect
    control_conn, _ = control_in_socket.accept()
    while True:
        # C <-> R 1
        msg_type = handle_status_request(control_conn)
        if msg_type == '16':
            break
        # C -> R 2
        filename = receive_choice_from_control(control_conn)
        if filename == '':  #we hit exit condition
            break
        #now we get to rendering...
        media_type, media_file = get_file_from_server(filename, server_out_socket)
        out_message = '13;' + media_type + ';'
        control_conn.send(out_message)


def handle_status_request(conn):
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

# TODO: How to take whole files from server help
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
    #what to do with media idk
    media_file = []
    return media_type, media_file


'''
#TODO: check media??
def check_correct_media(media_file, sock):
    
    return True
'''

#TODO: hmm txt... discussion?
def show_text(media_file):
    return

#TODO: Literally from stackoverflow
def play_video(media_file):
    capture  = cv.VideoCapture(0)

    nFrames = int(  cv.GetCaptureProperty(media_file, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty(media_file, cv.CV_CAP_PROP_FPS )
    frame_delay = int( 1/fps * 1000/1 )

    for f in xrange( nFrames ):
        frameImg = cv.QueryFrame(media_file)
        cv.ShowImage( "My Video Window",  frameImg )
        cv.WaitKey(frame_delay)

    # When playing is done, delete the window
    #  NOTE: this step is not strictly necessary, 
    #         when the script terminates it will close all windows it owns anyways
    cv.destroy_window( "My Video Window" )
    BUSY = False

#TODO: placeholder till we figure out how to do this
def receive_playback_command_from(sock):
    '''DO CERTAIN VIDEO THINGS BASED ON COMMAND FROM C'''
    return 0

main()