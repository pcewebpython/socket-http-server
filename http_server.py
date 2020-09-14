import socket
import sys
import traceback
import os
import mimetypes
import base64

def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    """

    # DONE: Implement response_ok

    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body
    ])


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # DONE: Implement response_method_not_allowed
    return b"\r\n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"",
        b"You can't do that on this server, 405 error Method Not Allowed!"
    ])
        


def response_not_found():
    """Returns a 404 Not Found response"""

    # DONE: Implement response_not_found
    return b"\r\n".join([
        b"HTTP/1.1 404 Not Found",
        b"",
        b"You can't do that on this server, 404 error Resource Name Not Found!"
    ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # DONE: implement parse_request

    method, path, version = request.split("\r\n")[0].split(" ")
    
    if method != "GET":
        raise NotImplementedError

    print("***MMM parse_request path= " + path)
    return path

def response_path(path):
    """
    This method should return appropriate content and a mime type.

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

    print("aaa")

    content = b"not implemented"
    mime_type = b"not implemented"
    
    print("bbb")
    
    fps = ('webroot\\' + path)
    print("response_path fps = " + str(fps))
    
    status_isfile = os.path.isfile('webroot\\' + path)
    print("response_path isfile status = " + str(status_isfile))

    print("ccc")

    status_isdir = os.path.isdir('webroot\\' + path)
    print("response_path isdir status = " + str(status_isdir))

    print("ddd")

    # DONE: Raise a NameError if the requested content is not present
    # under webroot.
    if ( (status_isfile == False) and (status_isdir == False) ):
        print("raise nameerror")
        raise NameError

    if (status_isfile):

        mime_type=b"text/plain"
        
        print("***MMM resource is a file fps =" + fps)
        
      
        filename, file_extension = os.path.splitext(fps)
        print(f"***MMM filename={filename}, extenstion={file_extension}")

        if (file_extension == ".html"):
            f=open(fps, "r")
            contents =f.read()
            f.close()
            print("***MMM text file contents =" + str(contents))
            content=contents.encode('utf-8')
            mime_type=b"text/html"
        elif (file_extension == ".txt"):
            f=open(fps, "r")
            contents =f.read()
            f.close()
            #print("***MMM text file contents =" + str(contents))
            content=contents.encode('utf-8')
            mime_type=b"text/plain"
        elif (file_extension == ".png"):
            print("2222222222 binary file read")

            f=open(fps,"rb")
            #ary_bytes=list(f.read())
            #contents = ""
            #contents = ''.join([str(elem) for elem in ary_bytes])
            ary_bytes = f.read()
            contents = ary_bytes
            print("***MMM binary file contents =" + str(contents))
            #content=contents.encode('utf-8')
            content=contents
            mime_type=b"image/png"
            
            #contents = base64.b64encode(open(fps, 'rb').read()).decode('utf-8')
            #content = contents
            #mime_type=b"image/png;base64"

            #f = open(fps, "rb")
            #byte = f.read(1)
            #while byte:
            #    print(byte)
            #    byte = f.read(1)

            

            f.close()
        elif (file_extension == ".jpg"):
            f=open(fps,"rb")
            ary_bytes = f.read()
            contents = ary_bytes
            #print("***MMM binary file contents =" + str(contents))
            content=contents
            mime_type=b"image/jpeg"
            f.close()

    elif (status_isdir):
        ary_files = os.listdir(fps)
        print(f"***MMM list of files in dir {ary_files}")
        str_files = '\n'.join(ary_files)
        content = str_files.encode('utf-8')
        mime_type=b"text/plain"
    

    print("***MMM file content encoded =" + str(content))
        
    # Done: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
        

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    #print("11111")
                    data = conn.recv(1024)
                    #print("22222")
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        #print("55555")
                        break

                    #print("44444")

                print("Request received:\n{}\n\n".format(request))

                try:
                
                    response = None
                    if (".ico" in request):
                        pass
                    else:
                
                        # DONE: Use parse_request to retrieve the path from the request.
                        path = parse_request(request)

                        # DONE: Use response_path to retrieve the content and the mimetype,
                        # based on the request path.
                        print("call response_path")
                        content, mime_type = response_path(path)

                        #print("***MMM response content encoded =" + str(content))
                        print("***MMM 1111111111111111111111111")
                        
                        
                        
                        # DONE: If no exceptions use the content and mimetype from response_path to build a 
                        # response_ok.
                        response = response_ok(content, mime_type)
                        
                        print("***MMM ***********************")
                        #print("88888 response = " + str(response))
                    
                except NameError:
                    # DONE; If response_path raised
                    # a NameError, then let response be a not_found response. Else,
                    response = response_not_found()
                except NotImplementedError:
                    # Done; If parse_request raised a NotImplementedError, then let
                    # response be a method_not_allowed response.
                    response = response_method_not_allowed()

                if (response is not None):
                    conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                print("***MMM closing connection")
                conn.close() 
                
    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)


