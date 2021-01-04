import socket
import sys
import os
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
    """
    print(mimetype)
    print(body)
    response = f"""HTTP/1.1 200 OK\r
Content-Type:{mimetype}\r\n\r
<html><body>{body}</body></html>\r
"""
    # response = "HTTP/1.1 200 OK\r\n"
    # response += "Content-Type:{}\r\n".format(mimetype)
    # response += "\r\n"
    # response += "html><body>{}</body></html>\r\n".format(body)

    return response.encode()

def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    response = f"""HTTP/1.1 405\r
Content-Type: text/plain\r\n\r
<html><body>Method Not Allowed</body></html>\r"""
    return response.encode()


def response_not_found():
    """Returns a 404 Not Found response"""

    response = f"""HTTP/1.1 404\r
                Content-Type: text/plain\r\n\r
                <html><body>Not Found</body></html>\r"""
    return response.encode()


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
    content = ""
    mime_type = ""
    path = f"webroot{path}"
    if not os.path.exists(path):
        raise NameError
    # TODO: Raise a NameError if the requested content is not present
    # under webroot.


    if os.path.isdir(path):
        dir_list = os.listdir(path)
        # dir_byte = "".join([str(elem + ", ") for elem in dir_list]).encode('utf8')
        print(dir_list)
        content = ''.join(dir_list).encode()
        mime_type = b"text/plain"

        print(content)

    if os.path.isfile(path):
        types = {".jpg": "image/jpeg", ".png": "image/png", ".html": "text/html", ".ico": "image/vnd.microsoft.icon", ".txt" : "text/plain"}
        name, extension = os.path.splitext(path)
        mime_type = types.get(extension)
        print(mime_type)

        with open(path, 'rt') as file:
            content = file.read()


    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.
    
    # content = b"not implemented"
    # mime_type = b"not implemented"

    return content, mime_type
# except NameError:
#     response = response_not_found()
#     # conn.sendall(response)


# def server(log_buffer=sys.stderr):
    # address = ('127.0.0.1', 10000)
    # sock = socket.socket(socket.AF_INET, 
    #                      socket.SOCK_STREAM, 
    #                      socket.IPPROTO_TCP)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permit reuse of local addresses for this socket
    # print("making a server on {0}:{1}".format(*address), file=log_buffer)
    # sock.bind(address)
    # sock.listen(1)

    # try:
    #     while True:
    #         print('waiting for a connection', file=log_buffer)
    #         conn, addr = sock.accept()  # blocking
    #         try:
    #             print('connection - {0}:{1}'.format(*addr), file=log_buffer)

    #             request = ''
    #             while True:
    #                 data = conn.recv(1024)
    #                 request += data.decode('utf8')

    #                 if '\r\n\r\n' in request:
    #                     break
		

    #             print("Request received:\n{}\n\n".format(request))


    #             path = parse_request(request)
    #             # TODO: Use parse_request to retrieve the path from the request.

    #             content, mime_type = response_path(path)
    #             # print(content)
    #             # print(mime_type)

    #             # TODO: Use response_path to retrieve the content and the mimetype,
    #             # based on the request path.
    #             # response = response_ok(
    #             #     body=content,
    #             #     mimetype=mime_type
    #             # )
    #             response = response_ok()

    #             # TODO; If parse_request raised a NotImplementedError, then let
    #             # response be a method_not_allowed response. If response_path raised
    #             # a NameError, then let response be a not_found response. Else,
    #             # use the content and mimetype from response_path to build a 
    #             # response_ok.
    #             # response = response_ok(
    #             #     body=b"Welcome to my web server",
    #             #     mimetype=b"text/plain"
    #             # )


    #             # response = response_ok(
    #             #         body=b"Welcome to my web server",
    #             #         mimetype=b"text/plain"
    #             #         )

    #             conn.sendall(response)

    #         except NotImplementedError:
    #             response = response_method_not_allowed()
    #         except NameError:
    #             response = response_not_found()
    #         except:
    #             traceback.print_exc()
    #         finally:
    #             pass
    #             # conn.close() 

    # except KeyboardInterrupt:
    #     sock.close()
    #     return
    # except:
    #     traceback.print_exc()

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
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break
		

                print("Request received:\n{}\n\n".format(request))

                # TODO: Use parse_request to retrieve the path from the request.
                path = parse_request(request)
                # TODO: Use response_path to retrieve the content and the mimetype,
                # based on the request path.
                content, mime_type = response_path(path)
                # TODO; If parse_request raised a NotImplementedError, then let
                # response be a method_not_allowed response. If response_path raised
                # a NameError, then let response be a not_found response. Else,
                # use the content and mimetype from response_path to build a 
                # response_ok.
                response = response_ok(
                    body=content,
                    mimetype=mime_type
                )
                print(response)
                conn.sendall(response)
            except NotImplementedError:
                response = response_method_not_allowed()
                conn.sendall(response)
            except NameError:
                response = response_not_found()
                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()



if __name__ == '__main__':
    # response = response_ok(
    #             body=b"Welcome to my web server",
    #             mimetype=b"text/plain"
    #             )
    # print(response)
    server()
    sys.exit(0)


