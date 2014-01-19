import socket
import sys
import os
import mimetypes

HOME = "webroot"

def response_not_found():
    return "HTTP/1.1 404 Not Found\r\n"

def resolve_uri(uri):

    relative_path = HOME + uri
    relative_path = os.path.normpath(relative_path)

    print >>sys.stderr, "URI:  %s" % uri
    print >>sys.stderr, "relative_path:  %s" % relative_path

    if not os.path.exists(relative_path):
        raise ValueError
        
    if os.path.isdir(relative_path):
        # If its a directory, return the plain text listing and the mime type
        # of "plain/text"
        listing = os.listdir(relative_path)
        return "\n".join(listing), "text/plain"
    
    elif os.path.isfile(relative_path):
        # The path is a file, return the file contents and mime type
        
        # Read in the file contents
        with open(relative_path, 'rb') as f:
            file_contents = f.read()
    
        # Get the file extension
        root, ext = os.path.splitext(uri)

        # Find the file's mime type
        mime_type = mimetypes.types_map[ext]
        return file_contents, mime_type

def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()

    if method == "GET":
        return uri
    
    else:
        raise NotImplementedError("We only accept GET")

def response_ok(body, mimetype):
    # First line of response contains version, status, reason followed by CRLF.
    r = "HTTP/1.1 200 OK" + "\r\n"
    # Each requests header field is followed by CRLF.
    r += ("Content-Type: %s" % mimetype) + "\r\n"
    # Another CRLF
    r += "\r\n"
    # Message body
    r += body
    return r

def response_method_not_allowed():
    not_allowed = "HTTP/1.1 405 Method Not Allowed\r\n"
    return not_allowed

def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>log_buffer, "making a server on {0}:{1}".format(*address)
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>log_buffer, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>log_buffer, 'connection - {0}:{1}'.format(*addr)
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break
                    
                try:
                    uri = parse_request(request)
                    file_contents, mime_type = resolve_uri(uri)
                    r = response_ok(file_contents, mime_type)

                except ValueError:
                    r = response_not_found()
                
                except NotImplementedError:
                    r = response_method_not_allowed()
                
                conn.sendall(r)

            finally:
                conn.close()
            
    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
