##python -u tcpprintserver.py
import socket

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8080))

server.listen(1)

n = 1

while 1:
    (client, address) = server.accept()
    request = ""
    while 1:
        chunk - client.recv(1)

        if chunk:
            request += chunk.decode()

        if request[-4:] = "\r\n\r\n":
            break

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text\r\n"
    respone += "\r\n"
    response += "You are the {}th visitor!".format(n)

    client.sendall(response.encode())

    client.close()
    print(request)

    n += 1