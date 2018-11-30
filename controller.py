'''Controller -> OUT TO BOTH R & S'''
#!/usr/bin/env python
import socket

TYPE = 0
CODE = 1
DATA = 2
BUFFER_SIZE = 1024

def main():
    ''' controller request list from server, send selection to renderer'''
    server_addr = '10.0.0.1'
    server_port = 5300
    server_out_socket = create_sender_socket(server_addr, server_port)
    render_addr = '10.0.0.2'
    render_port = 5400
    render_out_socket = create_sender_socket(render_addr, render_port)
    controller(server_out_socket, render_out_socket)
    disconnect_renderer(render_out_socket)
    render_out_socket.close()
    disconnect_server(server_out_socket)
    server_out_socket.close()


def controller(server_out_socket, render_out_socket):
    '''Given server, and renderer, work with both'''
    while True:
        print '\n\n--------------\nRequesting list from server'
        media_list = get_list_from_server(server_out_socket)
        # keep going while renderer is busy
        while True:
            selected_index = request_choice_from_user(media_list)
            if selected_index == -1:
                return   # We send exit code when render expects status request
            print 'Checking if renderer is busy...'
            # C <-> R 1
            if not renderer_busy(render_out_socket):
                break
            else:
                print 'Renderer is busy! Try again: '
        else:
            print 'Sending choice to Renderer...'
        selected_name = media_list[selected_index]
        print selected_name
        #C->R 2
        send_choice_to_renderer(selected_name, render_out_socket)
        receive_media_confirmation(render_out_socket)
        print 'Received media'

def create_sender_socket(addr, port):
    '''create, connect, return socket sending to certain ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    return sock
    

def disconnect_server(sock):
    '''Send message to terminate connection to S'''
    message = '3;0;'
    sock.send(message)
    print 'Disconnecting from server'


def disconnect_renderer(sock):
    '''Send message to terminate connection to R'''
    message = '16;0;'
    sock.send(message)
    print 'Disconnecting from renderer'


def get_list_from_server(sock):
    '''GET media list from server'''
    sock.send('1;0;')
    buffer_size = 1024
    response = sock.recv(buffer_size).split(';')
    if response[TYPE] == '0':
        return []
    elif response[TYPE] == '2':
        media_list = response[DATA].translate(None, '[]')
        media_list = media_list.split(',')
        for i in range(len(media_list)):
            media_list[i] = media_list[i].replace('\'','').strip()
        return media_list


def print_list(lst):
    '''Print list and indices to user'''
    index = 0
    for entry in lst:
        print str(index) + ': ' + entry
        index += 1


def receive_media_confirmation(render_out_socket):
    '''Get response from server about file metadata before rcv file'''
    while True:
        print 'hi2'
        in_message = render_out_socket.recv(BUFFER_SIZE).split(';')
        print in_message
        if in_message[TYPE] == '13':            
            break
    if in_message[CODE] == '0':
        text_playback(render_out_socket)
    elif in_message[CODE] == '1':
        video_playback(render_out_socket)
    else:
        print 'Media unavailable or inaccessible!'


def renderer_busy(sock):
    '''Send R status request, return whether R is busy'''
    sock.send('10;1;')
    while True:
        message = sock.recv(BUFFER_SIZE).split(';')
        if message[TYPE] == '11':
            break
    return message[CODE] == '1'


def request_choice_from_user(lst):
    '''Print list, get and validate user input, return choice '''
    print_list(lst)
    choice = raw_input('Select an option (or -1 to exit):')
    while (choice != '-1' and not choice.isdigit()) or (int(choice) \
        >= len(lst) or int(choice) < -1):
        choice = raw_input('Invalid input, try again: ')
    return int(choice)


def send_choice_to_renderer(filename, sock):
    '''Send media choice to renderer'''
    message = '12;0;' + filename
    sock.send(message)

# TODO: PLAYBACK COMMANDS HOW DO???
def text_playback(sock):
    '''Show text I guess...'''
    print 'Opening the text!'

    #idk what to do here tbh


def video_playback(sock):
    '''Get media, PLAY, PAUSE, ETC. RELAY TO RENDERER'''
    print 'Starting the video!'


main()
