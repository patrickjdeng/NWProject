#!/usr/bin/env python

#Renderer.py
#Zack Oldham
#11/04/2018
#The Renderer broadcasts its presence and waits for a connection from a controller.
#When a controller connects, it sends a request to renderer to get a file from the server which the renderer will then display as commanded by the controller. 


from socket import *

buffer_size = 1024
server_port = 8080


while True:
    rendererSocket = socket(AF_INET, SOCK_STREAM)
    rendererSocket.bind((gethostname(), 8000))
    rendererSocket.listen(1)

    print "waiting for connection..."
    controllerSocket = rendererSocket.accept()
    print "connection successful"
    

    #current status message from the controller
    recv_message = controllerSocket.recv(buffer_size) # recv_message = [type, code, data] --> data: None or [serverAddress, fileName]

    if message[0] = 5: #so far so good, controller is idle so communicate accordingly
        send_message = [6, 0, None]
        rendererSocket.send(send_message)
    else: #error occurred, terminate connection
        print "invalid controller message"
        send_message = [10, 1, None]
        controllerSocket.close()
        rendererSocket.close()


    while recv_message[0] != 10
        #File to Display message from controller
        recv_message = controllerSocket.recv(buffer_size)

        if message[0] == 3:
            if recv_message[2][0] == None or recv_message[2][1] == None:
                print "invalid file request: must provide server Address and file name"
                continue
            else:
                fileSocket = socket(AF_INET, SOCK_STREAM)
                fileSocket.connect((recv_message[2][0],server_port))
                send_message = [11, None, recv_message[2][1]]
                fileSocket.send(send_message)
                recv_message = fileSocket.recv(1024)

                if recv_message[0] != 12:
                    print "invalid response from server, try again"
                    continue
                elif recv_message[1] == 0:
                    print "file not found"
                    continue
                elif recv_message[1] == 1:
                    #display text file and process commands from controller as they arrive

                    #at some point controller is through and issues termination message causing inner loop to end
                    
                else:
                    #display video file and process commands from controller as they arrive
                    
                    #at some point controller is through and issues termination message causing inner loop to end 
                    

        else:
            print "invalid file request, try again"
            continue
        
            
        
        
        
    
    
    
    
    
