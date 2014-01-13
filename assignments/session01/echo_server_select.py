import socket
import sys
import select

def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # TODO: Replace the following line with your code which will instantiate 
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    
    # TODO: Set an option to allow the socket address to be reused immediately
    #       see the end of http://docs.python.org/2/library/socket.html
    # This is cool, didn't know I could do this.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # log that we are building a server
    print >>log_buffer, "making a server on {0}:{1}".format(*address)
    
    # TODO: bind your new sock 'sock' to the address above and begin to listen
    #       for incoming connections
    sock.bind(address)
    try:
        sock.listen(10)
        
        # Create a list of potential readers
        potential_readers = [sock]
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print >>log_buffer, 'waiting for a connection'

            ready_to_read, ready_to_write, in_error = select.select(potential_readers, [], [])
            for reader in ready_to_read:
                
                # If a client is trying to connect to the server, accept the
                # connection and then add it to the potential readers list.
                if reader == sock:
                    conn, addr = sock.accept()
                    potential_readers.append(conn)
                    print >>log_buffer, 'connection - {0}:{1}'.format(*addr)
                
                else:
                    # This is a client connection. Do the echo server stuff.
                    try:
                        data = reader.recv(16)
                    except:
                        # Client unexpectedly closed connection, handle it.
                        reader.close()
                        potential_readers.remove(reader)
                        
                    print >>log_buffer, 'received "{0}"'.format(data)

                    if data:
                        reader.sendall(data)
                    else:
                        reader.close()
                        potential_readers.remove(reader)
            
    except KeyboardInterrupt:
        # TODO: Use the python KeyboardIntterupt exception as a signal to 
        #       close the server socket and exit from the server function. 
        #       Replace the call to `pass` below, which is only there to 
        #       prevent syntax problems
        sock.close()
        return

if __name__ == '__main__':
    server()
    sys.exit(0)