import socket
import threading

# Server setup
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port for the server to listen on

# Global variables
users = {}  # Keep track of connected users: {username: socket}
messages = []  # Store last 2 messages

# Handle each client in a separate thread
def handle_client(conn, username):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("%post"):
                # Posting a message
                message = data[6:]  # Remove command part
                message_id = len(messages) + 1
                messages.append((message_id, username, message))
                if len(messages) > 2:  # Keep only the last 2 messages
                    messages.pop(0)
                broadcast(f"{username} posted: {message}")
            elif data.startswith("%users"):
                # Send list of users
                user_list = ", ".join(users.keys())
                conn.sendall(f"Users: {user_list}\n".encode())
            elif data.startswith("%message"):
                # Retrieve a specific message by ID
                try:
                    msg_id = int(data.split()[1])
                    msg = next((m for m in messages if m[0] == msg_id), None)
                    if msg:
                        conn.sendall(f"Message {msg[0]} by {msg[1]}: {msg[2]}\n".encode())
                    else:
                        conn.sendall(b"Message not found.\n")
                except:
                    conn.sendall(b"Invalid message ID.\n")
            elif data.startswith("%leave"):
                # Client leaves the group
                break
    finally:
        conn.close()
        remove_user(username)
        broadcast(f"{username} has left the group.")

# Notify all users about events
def broadcast(message):
    for user_conn in users.values():
        user_conn.sendall(f"{message}\n".encode())

# Remove a user from the global list
def remove_user(username):
    if username in users:
        del users[username]

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        conn.sendall(b"Enter a unique username: ")
        username = conn.recv(1024).decode('utf-8').strip()
        
        if username in users:
            conn.sendall(b"Username taken. Disconnecting.\n")
            conn.close()
            continue

        users[username] = conn
        print(f"{username} joined from {addr}")
        broadcast(f"{username} joined the group.")
        conn.sendall(f"Welcome, {username}! Recent messages: {messages}\n".encode())

        threading.Thread(target=handle_client, args=(conn, username)).start()

if __name__ == "__main__":
    start_server()


