'''RENDERER: IN FROM C, OUT TO S'''
#!/usr/bin/env python
import socket
import numpy
import cv2 as cv # must install externally!

TYPE = 0
CODE = 1
DATA = 2
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


def renderer(control_in_socket, server_out_socket):
    '''get filename from C, request from S, play from C'''
    # TODO: break when controller sends disconnect
    control_conn, _ = control_in_socket.accept()
    while True:
        receive_status_request_from(control_conn)
        file_index = receive_choice_from(control_conn)
        media_file = get_file_from(file_index, server_out_socket)
        incorrect_file = True
        while incorrect_file:
            incorrect_file = check_correct_media(media_file,control_in_socket)

#TODO: receive from controller, which is supposed to req status before sending choice
def receive_status_request_from(conn):
    '''listen for status requests from C until ready'''
    if BUSY:
        return
    else:
        return

#TODO: Now gets actual request from C, which knows R is ready now
def receive_choice_from(conn):
    '''RENDERER RECEIVE LIST CHOICE FROM C'''
    return 0

#TODO: How to take whole files from server help
def get_file_from(index, sock):
    '''RENDERER GET FILE FROM S'''
    return 0

#TODO: Communication between C and R here
def check_correct_media(media_file, sock):
    '''COMPARE RECEIVED FILE WITH REQUESTED FROM C'''
    return True


#TODO: Literally from stackoverflow
def play_video(media_file):
    cap = cv.VideoCapture(0)
    vidFile = cv.CaptureFromFile( '/home/mhughes/sintel_trailer-480p.mp4' )

    nFrames = int(  cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FPS )
    waitPerFrameInMillisec = int( 1/fps * 1000/1 )

    print 'Num. Frames = ', nFrames
    print 'Frame Rate = ', fps, ' frames per sec'

    for f in xrange( nFrames ):
        frameImg = cv.QueryFrame( vidFile )
        cv.ShowImage( "My Video Window",  frameImg )
        cv.WaitKey( waitPerFrameInMillisec  )

    # When playing is done, delete the window
    #  NOTE: this step is not strictly necessary, 
    #         when the script terminates it will close all windows it owns anyways
    cv.destroy_window( "My Video Window" )


def receive_playback_command_from(sock):
    '''DO CERTAIN VIDEO THINGS BASED ON COMMAND FROM C'''
    return 0

main()