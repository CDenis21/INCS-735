import socket
import threading
import time
import tkinter as tk
from tkinter import \
    messagebox

HOST = '173.52.98.239'  # localhost
PORT = 5004  # port number

# create socket object and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# create a tkinter GUI window
root = tk.Tk()
root.title("Chatroom")

# create label and entry box for username
username_label = tk.Label(root, text="Username:")
username_label.pack(side=tk.TOP)
username_entry = tk.Entry(root)
username_entry.pack(side=tk.TOP)

# create label and entry box for message
message_label = tk.Label(root, text="Message:")
message_label.pack(side=tk.LEFT)
message_entry = tk.Entry(root)
message_entry.pack(side=tk.LEFT)

# create text widget to display messages
messages_text = tk.Text(root)
messages_text.pack(side=tk.RIGHT)

def receive_previous_messages():
    # function to receive previous messages from server and insert into messages_text widget
    previous_messages = client_socket.recv(1024).decode('utf-8')
    messages_text.insert(tk.END, previous_messages)

# start a new thread to receive previous messages from the server
previous_messages_thread = threading.Thread(target=receive_previous_messages)
previous_messages_thread.start()

def receive_messages():
    # function to receive messages from server and update the messages_text widget
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            messages_text.insert(tk.END, message + "\n")
        except:
            break

# create function to send messages to the server
def send_message():
    # get the username and message from the entry boxes
    username = username_entry.get().strip()
    message = message_entry.get().strip()

    if username and message:
        # create a message string with the username, message, and timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message_str = f"{username} ({timestamp}): {message}\n"

        # send the message to the server and clear the message entry box
        client_socket.send(message_str.encode('utf-8'))
        message_entry.delete(0, tk.END)

# create button to send message
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

# start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()


def on_close_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        client_socket.close()
        exit(0)



# run the tkinter event loop
root.mainloop()