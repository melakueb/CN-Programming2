import socket
import threading

# Server details
HOST = '127.0.0.1'
PORT = 3000

# Group and message data structures
available_groups = ['Muchkin', 'EmeraldCity', 'YellowBrick', 'Quadling', 'Gillikin']
group_users = {group: set() for group in available_groups}  # Tracks users in each group
group_messages = {group: [] for group in available_groups}  # Tracks messages in each group
user_sockets = {}  # Tracks active user sockets
user_groups = {}  # Tracks groups joined by each user

# Broadcast a message to all users in a specific group
def broadcast_to_group(group, message, exclude_user=None):
    for username in group_users[group]:
        if username != exclude_user and username in user_sockets:
            user_sockets[username].sendall(message.encode())


# Handle individual client connections
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    client_socket.send("Enter username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    print(f"User {username} connected.")

    # Add the user to the socket dictionary and initialize groups
    user_sockets[username] = client_socket
    user_groups[username] = set()

    client_socket.send(f"Welcome {username}! Use %groups to see available groups.\n".encode())

    while True:
        try:
            # Receive a command from the client
            command = client_socket.recv(1024).decode().strip()
            if not command:
                break

            parts = command.split()
            cmd = parts[0]

            if cmd == "%groups":
                # Send the list of available groups
                client_socket.send(f"Available groups: {', '.join(available_groups)}\n".encode())

            elif cmd == "%groupjoin" and len(parts) > 1:
                # Join a specific group
                group = parts[1]
                if group in available_groups:
                    if group not in user_groups[username]:
                        user_groups[username].add(group)
                        group_users[group].add(username)
                        client_socket.send(f"Joined group {group}.\n".encode())
                        broadcast_to_group(group, f"{username} has joined the group.\n", username)
                    else:
                        client_socket.send("You are already a member of this group.\n".encode())
                else:
                    client_socket.send("Invalid group name.\n".encode())

            elif cmd == "%grouppost" and len(parts) > 2:
                # Post a message to the group
                group = parts[1]
                message = " ".join(parts[2:])
                if group in user_groups[username]:
                    msg_id = len(group_messages[group])
                    group_messages[group].append((msg_id, username, message))
                    broadcast_to_group(group, f"Message [{msg_id}] from {username}: {message}\n")
                else:
                    client_socket.send("You are not a member of this group.\n".encode())

            elif cmd == "%groupusers" and len(parts) > 1:
                # List users in the group
                group = parts[1]
                if group in user_groups[username]:
                    users = group_users[group]
                    client_socket.send(f"Users in {group}: {', '.join(users)}\n".encode())
                else:
                    client_socket.send("You are not a member of this group.\n".encode())

            elif cmd == "%groupmessage" and len(parts) > 2:
                # Fetch a specific message by ID from the group
                group = parts[1]
                msg_id = int(parts[2])
                if group in user_groups[username] and msg_id < len(group_messages[group]):
                    _, sender, content = group_messages[group][msg_id]
                    client_socket.send(f"Message {msg_id} from {sender}: {content}\n".encode())
                else:
                    client_socket.send("Message ID not found or you are not a member of this group.\n".encode())

            elif cmd == "%groupleave" and len(parts) > 1:
                # Leave a specific group
                group = parts[1]
                if group in user_groups[username]:
                    user_groups[username].remove(group)
                    group_users[group].remove(username)
                    client_socket.send(f"Left group {group}.\n".encode())
                    broadcast_to_group(group, f"{username} has left the group.\n", username)
                else:
                    client_socket.send("You are not a member of this group.\n".encode())

            elif cmd == "%post" and len(parts) > 1:
                # Post a message to the public board
                message = " ".join(parts[1:])
                if "Public" in user_groups[username]:
                    msg_id = len(group_messages["Public"])
                    group_messages["Public"].append((msg_id, username, message))
                    broadcast_to_group("Public", f"[Public] {username}: {message}\n")
                else:
                    client_socket.send("You are not in the public board. Use %join to join it.\n".encode())

            elif cmd == "%users":
                # List all users in the public group or a specific group
                group = "Public"
                if group in group_users:
                    users = group_users[group]
                    client_socket.send(f"Users in {group}: {', '.join(users)}\n".encode())
                else:
                    client_socket.send("No users found in the public group.\n".encode())

            elif cmd == "%leave":
                # Leave all groups and disconnect
                for group in user_groups[username]:
                    group_users[group].remove(username)
                user_groups[username].clear()
                client_socket.send("You have left all groups and the public board.\n".encode())
                break

        except Exception as e:
            print(f"Error handling command from {username}: {e}")
            break

    # Cleanup user
    if username in user_sockets:
        del user_sockets[username]
        for group in user_groups[username]:
            group_users[group].remove(username)
        del user_groups[username]
    client_socket.close()
    print(f"User {username} disconnected.")


def start_server():
    """Start the server and handle incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()


if __name__ == "__main__":
    start_server()
