#!/usr/bin/python3.4

import socket
import threading

def sendData(sock):
    data = input("Please enter your message: ")
    sock.sendall(bytes(data, "utf-8"))
    print ("Sent:     {}".format(data))

def receiveData(sock):
    received = sock.recv(1024)
    print ("Received: {}".format(received))

def main():
    #maybe come back and let the client choose the host+port
    HOST, PORT = "localhost", 2600
    #create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    running = True
    print("welcome to chat client, Ctrl+c to quit")
    
    try:
        #set up a loop that sends and receives data
        #connect to server
        sock.connect((HOST, PORT))
        threading.Thread(target=sendData(sock)).start()
        threading.Thread(target=receiveData(sock)).start()
        print("welcome to chat client, Ctrl+c to quit")
    except (KeyboardInterrupt, SystemExit):
        running = False
        sock.sendall(bytes('quit', "utf-8"))
        sock.close()
        raise
    finally:
        sock.close()

if __name__ == '__main__':
    main()
