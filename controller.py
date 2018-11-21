'''Controller'''
#!/usr/bin/env python
import socket

TYPE = 0
CODE = 1
DATA = 2

def controller():
    ''' controller request list from server, send selection to renderer'''
    addr = '10.0.0.1'
    server_port = 5300
    server_socket = create_sender_socket(addr, server_port)
    # render_port = 5400
    # render_socket = create_sender_socket(addr, render_port)
    selected_index = 0
    while selected_index != '-1':
        media_list = get_list_from(server_socket)
        selected_index = request_user_choice(media_list)
        if selected_index == '-1':
            break
        else:
            break
            # TODO: check if renderer is busy
         #   send_choice(selected_index, render_socket)
    # disconnect_renderer(render_socket)
    # render_socket.close()
    disconnect_server(server_socket)
    server_socket.close()


def create_sender_socket(addr, port):
    '''create, connect, return socket sending to certain ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    return sock


def get_list_from(sock):
    '''GET media list from server'''
    message = '1;0;'  # it'll request a list from the server
    print 'Requesting list from server'
    sock.send(message)
    buffer_size = 1024
    print 'Receiving list from server'
    response = sock.recv(buffer_size).split(';')
    media_list = response[DATA].translate(None, '[]')
    media_list = media_list.split(',')
    return media_list


def print_list(lst):
    '''Print list and indices to user'''
    index = 0
    for entry in lst:
        print str(index) + ': ' + entry
        index += 1


def request_user_choice(lst):
    '''Print list, get and validate user input, return choice '''
    print_list(lst)
    choice = raw_input('Select an option (or -1 to exit):')
    while int(choice) >= len(lst) or int(choice) < -1:
        choice = raw_input('Invalid input, try again')
    return choice


def send_choice(index, sock):
    '''Send media choice to renderer'''
    message = '10;0;' + str(index) 
    sock.send(message)

# TODO 
def send_playback_command(sock):
    '''PLAY, PAUSE, ETC. RELAY TO RENDERER'''
    return sock


def disconnect_server(sock):
    '''Send message to terminate connection to S'''
    message = '3;0;'
    sock.send(message)

def disconnect_renderer(sock):
    '''Send message to terminate connection to R'''
    message = '18;0;'
    sock.send(message)

controller()
