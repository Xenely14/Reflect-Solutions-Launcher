import cryptocode
import threading
import socket
import glob
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('178.250.158.150', 4075))
server.listen()


def client_socket_listener(client, address):
    while True:
        client_request = client.recv(1024).decode('utf-8')

        if str(client_request).startswith('trytoauth'):
            user_discord_id = client_request.split()[1]
            user_key = client_request.split()[2]

            print(user_discord_id, user_key)

        if str(client_request) == 'stop':
            client.send('stop'.encode('utf-8'))
            break

        time.sleep(0.01)


while True:
    client_socket, client_address = server.accept()
    answer = f'connected to server from {client_address[0]}:{client_address[1]} 1'.encode('utf-8')
    client_socket.send(answer)
    threading.Thread(target=client_socket_listener, args=(client_socket, client_address,)).start()
    print(f'New connection established with {client_address[0]}:{client_address[1]}')
    time.sleep(0.02)
