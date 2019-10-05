import socket
import sys
import traceback

def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->
        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body
    ])



def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    return b"\r\n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"",
        b"You can't do that on this server!"
    ])


def response_not_found():
    """Returns a 404 Not Found response"""

    return b"\r\n".join([
        b"HTTP/1.1 404 Page not found",
        b"",
        b"404 I could not find that page!"
    ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.
    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    method, path, version = request.split("\r\n")[0].split(" ")

    if method != "GET":
        raise NotImplementedError

    return path

def response_path(path):
    import os, mimetypes
    """
    This method should return appropriate content  (body) and a mime type
    based on a path.
    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.
    If the path is a file, it should return the contents of that file
    and its correct mimetype.
    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.
    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")
        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")
        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")
        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError
    """


    local_path = os.path.join(os.getcwd(), "webroot", path.strip('/'))

    if os.path.isfile(local_path):
    	content = b""
    	with open(local_path, "rb") as f:
    		byte = f.read(1)
    		while byte != b"":
    			content += byte
    			byte = f.read(1)
    	mime_type = mimetypes.guess_type(local_path)[0].encode()
    elif os.path.isdir(local_path):
    	# Option 1: content = str(os.listdir(absolute_path))
    	content = " ".join(os.listdir(local_path)).encode()
    	mime_type = b"text/plain"
    else:
    	raise NameError
    return content, mime_type



def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)

    try:
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("making a server on {0}:{1}".format(*address))
            sock.bind(address)
            sock.listen(1)
            print('waiting for a connection')
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr))

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break


                print("Request received:\n{}\n\n".format(request))

                try:
                    path = parse_request(request)
                    content, mime_type = response_path(path)

                except NameError:

                    response = response_not_found()
                except NotImplementedError:

                    response = response_method_not_allowed()
                else:

                    response = response_ok(body=content, mimetype=mime_type)
            except:
                traceback.print_exc()
            finally:
                conn.sendall(response)
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        print("Caught another exception")
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)
