#!/usr/bin/env python

#Renderer.py
#Zack Oldham
#11/04/2018
#The Renderer broadcasts its presence and waits for a connection from a controller.
#When a controller connects, it sends a request to renderer to get a file from the server which the renderer will then display as commanded by the controller. 


from socket import *

def run_renderer():
    buffer_size = 1024
    server_port = 12000

    rendererSocket = socket(AF_INET, SOCK_STREAM)
    rendererSocket.bind(('', server_port))
    rendererSocket.listen(1)

    while True:
        print "waiting for connection..."
        controllerSocket, controller_addr = rendererSocket.accept()
        print "connection successful"
        print controller_addr
        #current status message from the controller
        message = controllerSocket.recv(buffer_size).split(',') # recv_message = [type, code, data] --> data: None or [serverAddress, fileName]
        
        if message[0] == '5':     #so far so good, controller is idle so communicate accordingly
            send_message = '6, 0, None'
            rendererSocket.send(send_message)
        else: #error occurred, terminate connection
            print "invalid controller message"
            send_message = '10, 1, None'
            controllerSocket.close()
            rendererSocket.close()


        while message[0] != 10:
            #File to Display message from controller
            message = controllerSocket.recv(buffer_size).split(',')

            if message[0] == 3:
                if message[2][0] == None or message[2][1] == None:
                    print "invalid file request: must provide server Address and file name"
                    continue
                else:
                    fileSocket = socket(AF_INET, SOCK_STREAM)
                    fileSocket.connect((message[2][0],server_port))
                    send_message = [11, None, message[2][1]]
                    fileSocket.send(send_message)
                    message = fileSocket.recv(1024)

                    if message[0] != 12:
                        print "invalid response from server, try again"
                        continue
                    elif message[1] == 0:
                        print "file not found"
                        continue
                    elif message[1] == 1:
                        #display text file and process commands from controller as they arrive
                        continue
                        #at some point controller is through and issues termination message causing inner loop to end                    
                    else:
                        #display video file and process commands from controller as they arrive
                        continue
                        #at some point controller is through and issues termination message causing inner loop to end 
                        

            else:
                print "invalid file request, try again"
                continue
            
run_renderer()
