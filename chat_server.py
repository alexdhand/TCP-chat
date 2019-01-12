#!/usr/bin/python3.4

import socketserver
import threading
import select

#make a list of all handlers so that the RequestHandler can forward messages
#between them
handler_list = []

class RequestHandler(socketserver.StreamRequestHandler):
    """
    Base class for request handler classes.

This class is instantiated for each request to be handled.  The
constructor sets the instance variables request, client_address
and server, and then calls the handle() method.  To implement a
specific service, all you need to do is to derive a class which
defines a handle() method.

The handle() method can find the request as self.request, the
client address as self.client_address, and the server (in case it
needs access to per-server information) as self.server.  Since a
separate instance is created for each request, the handle() method
can define arbitrary other instance variariables.

    Makes the RequestHandler for the server.
    A new handler is instantiated for each connection
    Overwrite the handle() method to implement communication.

    
    """
    #override the __init__method of StreamRequestHandler
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        self.running = True # per connection
        try:
            self.handle()
        except ConnectionResetError as err:
            print ('{} disconnected.'.format(self.client_address))
            handler_list.remove(self)
            self.finish()
        finally:
            self.finish()
        
    def handle(self):
        handler_list.append(self)
        print ('Client at {} connected.'.format(self.client_address))
        
        client = ('Client at {} sent: '.format(self.client_address)).encode()
        

        #debug
       # print (handler_list)
        #print (self)
        #print (self.client_address)
       # print (self.client_address[0])
       # print (self.request)
        
        #use while loop and wait for data
        while self.running:
            data = self.rfile.readline()
            #data = str(self.request.recv(1024), 'ascii').encode()
            print ('{} wrote: {}'.format(self.client_address[0], data))
            #write the data back to the client, so they know it sent correctly
            #data_self = "you sent: {}".format(data.upper())'
            try:
                self.wfile.write(data.upper())
            except BrokenPipeError as err:
                print ('user at {} disconnected unexpectedly.'.format(self.client_address))
            #this loop should send the data back to all other connected clients
            for h in handler_list:
                #debug print ('handler:  {} self: {}'.format(h, self.request))
                if h != self:
                    try:
                        h.wfile.write(client + data)
                    except BrokenPipeError as err:
                        print ('user at {} disconnected unexpectedly.'.format(h))
                                  
            # if the user sends "quit", remove the handler from the list,
            # and clean up the connection for that user
            if data == b'quit':
                self.running = False
                handler_list.remove(self)
                self.finish()
                
            
                


class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass
    


def main():
    server = None
    #the host:port the server is listening on
    HOST, PORT = "localhost", 2600

    try:
        #bind to the host:port
        server = ChatServer((HOST, PORT), RequestHandler)
        
        print ("Chat server started on port {}".format(PORT))
        server.serve_forever()
        #activate the server, keep it going until keyboard interrupt Ctrl+c

    except KeyboardInterrupt as err:
        print("Server shutting down", err)
        # need to kill any active handlers somehow...
        # the server itself will stop, but the handler keeps the socket open
        # if there is an active connection left
        if server is not None:
            # shutdown() only stops the serve_forever() loop...
            server.shutdown()
        
            
            
#call main
if __name__ == "__main__":
    main()
    # so from what i read, this will give the module more flexibility for when
    # it is imported by another module
