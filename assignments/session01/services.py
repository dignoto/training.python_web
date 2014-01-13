import socket
import sys

def main(begin_port, end_port):
    
    print "Printing services in port range %s to %s" % (begin_port, end_port)
    # Make sure we are given a valid port range
    if (begin_port < 0) or (end_port > 65535) or (begin_port > end_port):
        print >> sys.stderr, "Not a valid port range"
        return -1

    # For each port in the given range, print the service
    for port in xrange(begin_port, end_port + 1):
        try:
            print "Port:  %s, Service:  %s" % (port, socket.getservbyport(port))
        except:
            # Silently suppress exceptions for ports that we don't know a
            # service for.
            pass

    # Return success
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usg = '\nusage: python services.py 10 20\n'
        print >>sys.stderr, usg
        sys.exit(1)
    begin_port = int(sys.argv[1])
    end_port = int(sys.argv[2])
    sys.exit(main(begin_port, end_port))