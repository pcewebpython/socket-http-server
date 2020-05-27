import socket
import sys
import traceback
import webroot
import mimetypes
import os
import io
from contextlib import redirect_stdout


def response_ok(content=b"This is a minimal response", mimetype=b"text/plain"):
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

    # TODO: Implement response_ok
    # Needs to make use of body and MIME type argument.
    return b"\r\n".join([
                        b"HTTP/1.1 200 OK",
                        b"Content-Type: " + mimetype,
                        b"",
                        content,
                        ])


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # TODO: Implement response_method_not_allowed
    return b"\r\n".join([
                        b"HTTP/1.1 405 Method Not Allowed",
                        b"",
                        b"You can't do that on this server!"
                        ])


def response_not_found():
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found
    return b"\r\n".join([
                        b"HTTP/1.1 404 Not Found",
                        b"",
                        b"Resource not on on this server!"
                        ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # TODO: implement parse_request
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

    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.

    full_path = os.getcwd() + '/webroot/' + path

    directory = ['/']
    os.chdir(os.getcwd() + '/webroot')
    walk_result = os.walk('.')
    for line_result in walk_result:
        if line_result[1] != []:
            for dir_result in line_result[1]:
                directory.append('/' + line_result[0][1:] + dir_result)
                directory.append('/' + line_result[0][1:] + dir_result + '/')
        for file_result in line_result[2]:
            directory.append(line_result[0][1:] + '/' + file_result)
    os.chdir('..')

    if path not in directory:
        raise NameError

    elif '.' not in path:
        mime_type = b'text/plain'
        os.chdir(os.getcwd() + '/webroot')
        path_result = os.walk('.' + path)
        content_uncoded = ''
        for path_result_item in path_result:
            content_uncoded += str(path_result_item)
        content = content_uncoded.encode('utf8')
        os.chdir('..')

    else:
        mime_type = mimetypes.guess_type(path)[0].encode('utf8')
        content = b''
        if mime_type == b'text/html':
            with open(full_path, 'r') as html_file:
                for line in html_file.readlines():
                    content += line.encode('utf8')

        if mime_type[:5] == b'image':
            with open(full_path, 'rb') as image_file:
                for line in image_file.readlines():
                    content += line

        if mime_type == b'text/plain':
            with open(full_path, 'r') as plain_text_file:
                for line in plain_text_file.readlines():
                    content += line.encode('utf8')

        if mime_type == b'text/x-python':
            content_uncoded_1 = ''
            content_uncoded_2 = ''
            with open(full_path, 'r') as python_file, open('.temp_space.html', 'w') as exec_file:
                for line in python_file.readlines():
                    content_uncoded_1 += line
                f1 = io.StringIO()
                with redirect_stdout(f1):
                    exec(content_uncoded_1)
                exec_file.writelines(f1.getvalue())
            with open(os.getcwd() + '/.temp_space.html', 'r') as run_file:
                for line in run_file.readlines():
                    content_uncoded_2 += line
                content += content_uncoded_2.encode('utf8')
                mime_type = b'text/html'

    # content = b"not implemented"
    # mime_type = b"not implemented"

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
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                print("Request received:\n{}\n\n".format(request))

                # TODO: Use parse_request to retrieve the path from the request.
                try:
                    path = parse_request(request)
                    # print('hey path is {}'.format(path))

                    # TODO: Use response_path to retrieve the content and the mimetype,
                    # based on the request path.

                    content, mime_type = response_path(path)

                    # TODO; If parse_request raised a NotImplementedError, then let
                    # response be a method_not_allowed response. If response_path raised
                    # a NameError, then let response be a not_found response. Else,
                    # use the content and mimetype from response_path to build a
                    # response_ok.

                    response = response_ok(
                        content=content,
                        mimetype=mime_type
                    )

                    # response = response_ok(
                    #     content=b"Welcome to my web server!",
                    #     mimetype=b"text/plain"
                    # )

                except NotImplementedError:
                    response = response_method_not_allowed()

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
    server()
    sys.exit(0)
