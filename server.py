# Created by Helga on 06.05.2021
import socket
import threading


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('', 80))
    except OSError:
        sock.bind(('', 8000))
    sock.listen()
    print("Working on: http://127.0.0.1/")
    while True:
        client_socket, address = sock.accept()
        print("Connected", address)
        # data = client_socket.recv(1024).decode('utf-8')
        # connect = load_page(data)
        # client_socket.send(connect)
        # client_socket.shutdown(socket.SHUT_WR)
        tServer = threading.Thread(target=get_data, args=(client_socket,))
        tServer.start()


def get_data(client_socket):
    data = 1
    while data:
        data = client_socket.recv(1024).decode('utf-8')
        # print(data)
        if data:
            connect = load_page(data)
            client_socket.send(connect)
    # client_socket.shutdown(socket.SHUT_WR)

def load_page(request_data):
    global old_path
    # print('ДАТА', request_data)
    HDRS = 'HTTP/1.0 200 OK\r\nContent - Type: text / html;charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.0 404 OK\r\nContent - Type: text / html;charset=utf-8\r\n\r\n'
    if len(request_data) > 0:
        path = request_data.split(' ')[1]
        if path == "/":
            path = "/index.html"
    else:
        path = old_path

    response = ''
    try:
        with open('template' + path, 'rb') as file:  # rb байтовое представление
            response = file.read()
            old_path = path
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + '<h1> No such page exists</h1>').encode('utf-8')


if __name__ == '__main__':
    old_path = "/"
    start_server()
