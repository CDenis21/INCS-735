import socket
import threading
import time
import json

# Server configuration
HOST = '127.0.0.1' # localhost
PORT = 50000

# Data storage
messages = []  # list of dictionaries with timestamp and message
users = set()  # set of usernames

# Load previously saved data from file
try:
    with open('chat_data.json', 'r') as f:
        data = json.load(f)
        messages = data['messages']
        users = set(data['users'])
except:
    pass

# Function to save data to file
def save_data():
    data = {'messages': messages, 'users': list(users)}
    with open('chat_data.json', 'w') as f:
        json.dump(data, f)

# Function to broadcast message to all clients
def broadcast(message, username):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    messages.append({'timestamp': timestamp, 'message': f'{username}: {message}'})
    for client in clients:
        client.sendall(f'{timestamp} {username}: {message}'.encode())


# Function to handle client connections
def handle_client(client_socket):
    # Get username from client
    username = client_socket.recv(1024).decode()
    users.add(username)
    print(f'New connection from {username}')

    # Send welcome message and previously sent messages
    client_socket.sendall(f'Welcome to the chatroom, {username}!\n'.encode())
    for message in messages:
        client_socket.sendall(f'{message["timestamp"]} {message["message"]}\n'.encode())


    # Receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if message:
                broadcast(message, username)
        except:
            # Remove user and close connection
            print(f'{username} disconnected')
            users.remove(username)
            client_socket.close()
            clients.remove(client_socket)
            save_data()
            break

# Start server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f'Server listening on {HOST}:{PORT}')

# Accept incoming connections and start threads to handle them
clients = []
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

# server is hypothetically suppose to always active
# if need to terminate must be done force terminate from console
