# import socket
# import threading
# from datetime import datetime

# # Data structures
# users = {}  # Maps client sockets to usernames
# messages = []  # Stores public messages
# groups = {f"group{i}": [] for i in range(1, 6)}  # Predefined groups and their members

# # Format message for storage/display
# def format_message(msg_id, sender, timestamp, subject, content):
#     return f"{msg_id}, {sender}, {timestamp}, {subject}, {content}"

# def broadcast_message(message, exclude_socket=None):
#     """Sends a message to all connected clients except the sender."""
#     for client_socket in users:
#         if client_socket != exclude_socket:
#             client_socket.sendall(message.encode())

# def handle_client(client_socket):
#     """Handles communication with a connected client."""
#     try:
#         # Receive username
#         client_socket.sendall(b"Enter your username: ")
#         username = client_socket.recv(1024).decode().strip()
#         while username in users.values():
#             client_socket.sendall(b"Username taken. Enter another: ")
#             username = client_socket.recv(1024).decode().strip()

#         users[client_socket] = username
#         broadcast_message(f"{username} has joined the public board.\n")

#         # Send last 2 messages
#         last_messages = "\n".join(messages[-2:])
#         client_socket.sendall(f"Last messages:\n{last_messages if last_messages else 'No messages yet.'}\n".encode())

#         # Command loop
#         while True:
#             client_socket.sendall(b"Enter command: ")
#             command = client_socket.recv(1024).decode().strip()

#             if command == "%leave":
#                 client_socket.sendall(b"Leaving the group.\n")
#                 break

#             elif command == "%post":
#                 client_socket.sendall(b"Enter subject: ")
#                 subject = client_socket.recv(1024).decode().strip()
#                 client_socket.sendall(b"Enter content: ")
#                 content = client_socket.recv(1024).decode().strip()

#                 msg_id = len(messages) + 1
#                 timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 message = format_message(msg_id, username, timestamp, subject, content)
#                 messages.append(message)
#                 broadcast_message(f"New message: {message}\n")

#             elif command == "%users":
#                 client_socket.sendall(f"Users: {', '.join(users.values())}\n".encode())

#             elif command == "%groups":
#                 client_socket.sendall(f"Available groups: {', '.join(groups.keys())}\n".encode())

#             elif command.startswith("%groupjoin"):
#                 _, group = command.split()
#                 if group in groups:
#                     groups[group].append(username)
#                     client_socket.sendall(f"Joined {group}\n".encode())
#                 else:
#                     client_socket.sendall(b"Group not found.\n")

#             elif command.startswith("%groupleave"):
#                 _, group = command.split()
#                 if group in groups and username in groups[group]:
#                     groups[group].remove(username)
#                     client_socket.sendall(f"Left {group}\n".encode())
#                 else:
#                     client_socket.sendall(b"Not a member of this group.\n")

#             elif command.startswith("%groupusers"):
#                 _, group = command.split()
#                 if group in groups:
#                     members = groups[group]
#                     client_socket.sendall(f"Members of {group}: {', '.join(members)}\n".encode())
#                 else:
#                     client_socket.sendall(b"Group not found.\n")

#             elif command.startswith("%message"):
#                 # Extract the message ID
#                 parts = command.split()
#                 if len(parts) != 2 or not parts[1].isdigit():
#                     client_socket.sendall(b"Invalid message ID format. Usage: %message [ID]\n")
#                     continue
                
#                 msg_id = int(parts[1]) - 1  # Convert to 0-based index
#                 if 0 <= msg_id < len(messages):
#                     client_socket.sendall(f"Message {msg_id + 1}: {messages[msg_id]}\n".encode())
#                 else:
#                     client_socket.sendall(b"Message ID not found.\n")

#             else:
#                 client_socket.sendall(b"Invalid command.\n")
#     finally:
#         username = users.pop(client_socket, None)
#         broadcast_message(f"{username} has left the public board.\n")
#         client_socket.close()

# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(("0.0.0.0", 12345))
#     server.listen(5)
#     print("Server is running on port 12345...")

#     while True:
#         client_socket, _ = server.accept()
#         threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

# if __name__ == "__main__":
#     main()


# claude below

import socket
import threading
import json
from datetime import datetime

# Server configuration
HOST = 'localhost'
PORT = 12345
MAX_CLIENTS = 100

# Data structures to store group and user information
groups = {
    'public': {'messages': [], 'users': []},
    'group1': {'messages': [], 'users': []},
    'group2': {'messages': [], 'users': []},
    'group3': {'messages': [], 'users': []},
    'group4': {'messages': [], 'users': []},
    'group5': {'messages': [], 'users': []}
}

# Lock for synchronizing access to shared data
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    user = None
    current_group = None

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        command = data.split()[0]

        if command == '%connect':
            user = data.split()[1]
            conn.send("Connected to server.".encode())

        elif command == '%join':
            if user:
                with lock:
                    groups['public']['users'].append(user)
                    current_group = 'public'
                conn.send(f"Joined group: {current_group}".encode())
                broadcast_message(f"{user} joined the group.", current_group, user)
                send_user_list(conn, current_group)
                send_last_messages(conn, current_group)
            else:
                conn.send("Please connect to the server first.".encode())

        elif command == '%post':
            if user and current_group:
                subject = data.split()[1]
                message = ' '.join(data.split()[2:])
                post_message(user, subject, message, current_group)
                broadcast_message(f"{user} posted a new message.", current_group, user)
            else:
                conn.send("Please join a group first.".encode())

        elif command == '%users':
            if current_group:
                send_user_list(conn, current_group)
            else:
                conn.send("Please join a group first.".encode())

        elif command == '%leave':
            if user and current_group:
                with lock:
                    groups[current_group]['users'].remove(user)
                conn.send(f"Left group: {current_group}".encode())
                broadcast_message(f"{user} left the group.", current_group, user)
                current_group = None
            else:
                conn.send("Please join a group first.".encode())

        elif command == '%message':
            if user and current_group:
                message_id = int(data.split()[1])
                send_message_content(conn, current_group, message_id)
            else:
                conn.send("Please join a group first.".encode())

        elif command == '%exit':
            break

        elif command == '%groups':
            send_group_list(conn)

        elif command == '%groupjoin':
            if user:
                group_name = data.split()[1]
                if group_name in groups:
                    with lock:
                        groups[group_name]['users'].append(user)
                        current_group = group_name
                    conn.send(f"Joined group: {current_group}".encode())
                    broadcast_message(f"{user} joined the group.", current_group, user)
                    send_user_list(conn, current_group)
                    send_last_messages(conn, current_group)
                else:
                    conn.send("Invalid group name.".encode())
            else:
                conn.send("Please connect to the server first.".encode())

        elif command == '%grouppost':
            if user and current_group:
                group_name = data.split()[1]
                subject = data.split()[2]
                message = ' '.join(data.split()[3:])
                post_message(user, subject, message, group_name)
                broadcast_message(f"{user} posted a new message.", group_name, user)
            else:
                conn.send("Please join a group first.".encode())

        elif command == '%groupusers':
            group_name = data.split()[1]
            send_user_list(conn, group_name)

        elif command == '%groupleave':
            if user and current_group:
                group_name = data.split()[1]
                with lock:
                    groups[group_name]['users'].remove(user)
                conn.send(f"Left group: {group_name}".encode())
                broadcast_message(f"{user} left the group.", group_name, user)
                if group_name == current_group:
                    current_group = None
            else:
                conn.send("Please join a group first.".encode())

        elif command == '%groupmessage':
            if user:
                group_name = data.split()[1] 
                message_id = int(data.split()[2])
                send_message_content(conn, group_name, message_id)
            else:
                conn.send("Please join a group first.".encode())

        else:
            conn.send("Invalid command.".encode())

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def post_message(user, subject, message, group_name):
    with lock:
        message_id = len(groups[group_name]['messages']) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        groups[group_name]['messages'].append({
            'id': message_id,
            'sender': user,
            'subject': subject,
            'message': message,
            'timestamp': timestamp
        })

def broadcast_message(message, group_name, sender):
    with lock:
        for user in groups[group_name]['users']:
            if user != sender:
                user_conn = get_user_connection(user)
                if user_conn:
                    user_conn.send(message.encode())

def send_user_list(conn, group_name):
    with lock:
        user_list = ", ".join(groups[group_name]['users'])
        conn.send(f"Users in {group_name} group: {user_list}".encode())

def send_last_messages(conn, group_name):
    with lock:
        last_messages = groups[group_name]['messages'][-2:]
        for message in last_messages:
            conn.send(f"{message['id']}, {message['sender']}, {message['timestamp']}, {message['subject']}".encode())

def send_message_content(conn, group_name, message_id):
    with lock:
        for message in groups[group_name]['messages']:
            if message['id'] == message_id:
                conn.send(json.dumps(message).encode())
                return
        conn.send("Message not found.".encode())

def send_group_list(conn):
    group_list = ", ".join(groups.keys())
    conn.send(f"Available groups: {group_list}".encode())

def get_user_connection(user):
    for conn, addr in client_conns:
        if user == user_conns[conn]:
            return conn
    return None

# Start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CLIENTS)
print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

# Store client connections and associated users
client_conns = []
user_conns = {}

while True:
    conn, addr = server_socket.accept()
    client_conns.append((conn, addr))
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")