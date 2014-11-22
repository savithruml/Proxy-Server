import socket
import threading
import re
import sys
import logging
import time
import os
import os.path

size = 4096                                              #buffer size of the receiver
path = "/Users/savithru/Desktop/prog3/temp1"             #Path specified for caching directory

logging.basicConfig(level=logging.INFO, filename='proxyserver.log', format='[%(levelname)s] %(asctime)s %(threadName)s %(message)s', ) 

#MAIN PROGRAM MODULE

def main():
    
    host = ''                                            #Localhost or 127.0.0.1
    port = 9601                                       #Port Number for the Proxy Server

#CREATE SOCKET & BIND 

    priSocket = None                                    #Intialize the primary socket
    
    try:
        priSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        priSocket.bind((host, port))
        print "The proxy is running on IP address 127.0.0.1 & on PORT number", port
        logging.info("The proxy is running on IP address 127.0.0.1 & on PORT number {}".format(port))
        priSocket.listen(100)         #Specifies the maximum number of connection in queue before rejecting connections

    except socket.error, (message):
        if priSocket:
            priSocket.close()                              #Add Exception if error has occured
        print 'Binding Error Encountered:', message
        sys.exit(1)

#WAIT FOR REQUEST. CREATE A NEW PROXY THREAD FOR EVERY REQUEST RECEIVED
    
    while 1:
        clientSocket, clientAddress = priSocket.accept()
        threadHTTP = threading.Thread(target=handler, args=(clientSocket, clientAddress))
        threadHTTP.start()

    priSocket.close()

#PROXY THREAD TO THE SERVER

def handler(clientSocket, clientAddress):

    request = clientSocket.recv(size)
    #print 'request:',request
    a = request.split(" ")[1]
    #print 'a:', a 
    b = a.split("/")[3]                         #Get the last part of the URL
    #print 'b:', b

 #ADD EXCEPTION TO BLOCK JPG FETCH

    if b.endswith(".jpg"):						#If URL ends with .jpg then send error 501 & exit
        #print "yes"						
        clientSocket.send('HTTP/1.1 501 OK\n Content-Type: text/html \n\n <HTML> <h1> 501 : File Type Not Supported</h1> </HTML>')
        sys.exit(1)

    hostName = ''
    port = 80                                   #Define standard port of 80 for HTTP requests from the proxy server
    
    for line in request.split('\n'):

        if line[0:4] == 'Host' or line[0:4] == 'From':
            hostName = line.split(' ')[1]                  #Gets the Host Name requested
            #print hostName
            hostName = hostName.strip()
            #print hostName
            #print "The hostname entered is ", hostName
            logging.info("The hostname entered is {}".format(hostName)) 
            break
            
#SEND REQUEST TO SERVER

    hostip = socket.gethostbyname(hostName)                          #Get the IP address of the Host Name requested
    print ("Hostname: {} & HostIP: {} ".format(hostName, hostip))
    logging.info("The user is trying to reach {} on port {}".format(hostip, port))
    
    try:
        serverSocket = socket.create_connection((hostName, port))    #Create_connection is used to create a socket since hostName can be non-numeric
        serverSocket.sendall(request)                                #Send all the requests from client to server

        data_received = 0                                  #Intialize the data received parameter

        
        serverSocket.settimeout(25)                        #Set a timeout = 25 seconds for the server session 
        clientSocket.settimeout(25)                        #Set a timeout = 25 seconds for the client session 
        dr_1 = os.getcwd()                                 #Get the present working directory
        #print dr_1 + '++++'

 #CACHE TIMER SET TO EXPIRE THE CACHE FILES AFTER 300 SECONDS       

        cacheTimer = time.time() - 300                      #Set cache timer to 300 seconds 
        os.chdir(path)                                     #Set directory path to cache the files 
        #dr_2 = os.getcwd()
        #print dr_2 + '----'

        for cachefile in os.listdir(path):
            #print os.listdir(path)
            st=os.stat(cachefile)
            mtime=st.st_mtime
            if mtime < cacheTimer:
                #print "File removed:", cachefile
                logging.info("File {} removed".format(cachefile))
                os.unlink(cachefile)                       #Remove the cache files if timer is expired 

#CHECK FOR FILE IN CACHE & SEND IF FILE EXISTS

        if os.path.isfile(hostName):
            rd = open(hostName, "r")                       #Open the file stored & send to client
            cacheData = rd.read()                          
            clientSocket.send(cacheData)    
            print "data sent from cache"
            #logging.info("Data sent from Cache {}".format(cacheData))
            serverSocket.close()
            clientSocket.close()

#FETCH FROM THE SERVER IF FILE NOT FOUND IN THE CACHE             
        
        while 1:                                            
            response = serverSocket.recv(size)                                                    #Receive data of size 4096
            data_received = data_received + len(response)   
            #print ("Data Received so far  from {} is {}".format(hostName, data_received))
            logging.info("Data received so far from {} is {}".format(hostName, data_received))    #Continuosly log the data received 
           
#STORE THE RECEIVED DATA ON TO THE CACHE 

            rw =  open(hostName, "a")
            rw.write(response)
            clientSocket.send(response)                         #Store the data received on to the cache directory 
            if response is None:
                break

        rw.close()                                              #Close the file
        
        serverSocket.close()                                    #Close the sockets after data is received
        clientSocket.close()
        
#CLOSE THE SOCKET IF REQUEST TO THE SERVER CANNOT BE SENT

    except socket.error, (message):
        if serverSocket:
            serverSocket.close()
        if clientSocket:                                        #Add exception if error has occured & close the sockets
            clientSocket.close()
        logging.info("Error: Socket Closed".format(message))
        sys.exit(1)

if __name__ == '__main__':
    main()
