import socket
import threading
import time

# Server configuration
HOST = '127.0.0.1' # localhost
PORT = 50000

# Function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            break

# Function to safely terminate the client connection
def stop_client():
    print('Closing connection...')
    client_socket.close()
    exit()

# Connect to server and send username
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
username = input('Enter your username: ')
client_socket.sendall(username.encode())

# Start thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Send messages to server
while True:
    
    # type in LOG OFF (all caps) for client to safely disconnect
    message = input()
    if message == 'LOG OFF':
        stop_client()
    if message:
        client_socket.sendall(message.encode())
    time.sleep(0.1)
