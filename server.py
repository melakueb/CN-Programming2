# server.py
import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 3000

usernames = {}
public_group = {
    'clients': [],
    'messages': []
}
groups = {
    'group1': {'clients': [], 'messages': []},
    'group2': {'clients': [], 'messages': []},
    'group3': {'clients': [], 'messages': []},
    'group4': {'clients': [], 'messages': []},
    'group5': {'clients': [], 'messages': []},
}

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    conn.send("Enter a username: ".encode())
    username = conn.recv(1024).decode().strip()

    while username in usernames.values():
        conn.send("Username already taken. Enter a different username: ".encode())
        username = conn.recv(1024).decode().strip()

    usernames[conn] = username
    conn.send(f"Welcome, {username}!".encode())
    print(f"{username} has connected.")

    user_in_public = False
    user_groups = set()

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                remove_client(conn, user_in_public, user_groups)
                break
            if data.startswith('%join'):
                if not user_in_public:
                    public_group['clients'].append(conn)
                    user_in_public = True
                    conn.send("You have joined the public message board.".encode())
                    # Notify others
                    broadcast(f"{username} has joined the public message board.", conn, public_group['clients'])
                    # Send last two messages
                    if len(public_group['messages']) >= 2:
                        for msg in public_group['messages'][-2:]:
                            msg_summary = f"{msg['id']}, {msg['sender']}, {msg['date']}, {msg['subject']}"
                            conn.send(msg_summary.encode())
                    # Send users list
                    user_list = ', '.join([usernames[c] for c in public_group['clients']])
                    conn.send(f"Users in the public group: {user_list}".encode())
                else:
                    conn.send("You have already joined the public message board.".encode())
            elif data.startswith('%post'):
                if user_in_public:
                    parts = data.split(' ', 2)
                    if len(parts) < 3:
                        conn.send("Usage: %post [subject] [content]".encode())
                        continue
                    subject = parts[1]
                    content = parts[2]
                    message_id = len(public_group['messages']) + 1
                    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = {
                        'id': message_id,
                        'sender': username,
                        'date': post_date,
                        'subject': subject,
                        'content': content
                    }
                    public_group['messages'].append(message)
                    message_summary = f"{message_id}, {username}, {post_date}, {subject}"
                    broadcast(message_summary, conn, public_group['clients'])
                    conn.send("Message posted to the public message board.".encode())
                else:
                    conn.send("You need to join the public message board first using %join.".encode())
            elif data.startswith('%users'):
                if user_in_public:
                    user_list = ', '.join([usernames[c] for c in public_group['clients']])
                    conn.send(f"Users in the public group: {user_list}".encode())
                else:
                    conn.send("You are not in the public message board. Use %join to join.".encode())
            elif data.startswith('%leave'):
                if user_in_public:
                    public_group['clients'].remove(conn)
                    user_in_public = False
                    broadcast(f"{username} has left the public message board.", conn, public_group['clients'])
                    conn.send("You have left the public message board.".encode())
                else:
                    conn.send("You are not in the public message board.".encode())
            elif data.startswith('%message'):
                if user_in_public:
                    parts = data.split()
                    if len(parts) != 2:
                        conn.send("Usage: %message [message ID]".encode())
                        continue
                    msg_id = int(parts[1])
                    if 1 <= msg_id <= len(public_group['messages']):
                        msg = public_group['messages'][msg_id - 1]
                        msg_content = f"Message {msg['id']} Content:\nSender: {msg['sender']}\nDate: {msg['date']}\nSubject: {msg['subject']}\nContent: {msg['content']}"
                        conn.send(msg_content.encode())
                    else:
                        conn.send("Message ID not found.".encode())
                else:
                    conn.send("You are not in the public message board. Use %join to join.".encode())
            elif data.startswith('%groups'):
                group_list = ', '.join(groups.keys())
                conn.send(f"Available groups: {group_list}".encode())
            elif data.startswith('%groupjoin'):
                parts = data.split()
                if len(parts) != 2:
                    conn.send("Usage: %groupjoin [group name]".encode())
                    continue
                group_name = parts[1]
                if group_name in groups:
                    if group_name not in user_groups:
                        groups[group_name]['clients'].append(conn)
                        user_groups.add(group_name)
                        conn.send(f"You have joined group {group_name}.".encode())
                        group_broadcast(f"{username} has joined group {group_name}.", conn, group_name)
                        # Send last two messages
                        group_msgs = groups[group_name]['messages']
                        if len(group_msgs) >= 2:
                            for msg in group_msgs[-2:]:
                                msg_summary = f"{msg['id']}, {msg['sender']}, {msg['date']}, {msg['subject']}"
                                conn.send(f"[{group_name}] {msg_summary}".encode())
                    else:
                        conn.send(f"You are already a member of group {group_name}.".encode())
                else:
                    conn.send("Group does not exist.".encode())
            elif data.startswith('%grouppost'):
                parts = data.split(' ', 3)
                if len(parts) < 4:
                    conn.send("Usage: %grouppost [group name] [subject] [content]".encode())
                    continue
                group_name = parts[1]
                if group_name in user_groups:
                    subject = parts[2]
                    content = parts[3]
                    message_id = len(groups[group_name]['messages']) + 1
                    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = {
                        'id': message_id,
                        'sender': username,
                        'date': post_date,
                        'subject': subject,
                        'content': content
                    }
                    groups[group_name]['messages'].append(message)
                    message_summary = f"{message_id}, {username}, {post_date}, {subject}"
                    group_broadcast(f"[{group_name}] {message_summary}", conn, group_name)
                    conn.send(f"Message posted to group {group_name}.".encode())
                else:
                    conn.send("You are not a member of this group.".encode())
            elif data.startswith('%groupusers'):
                parts = data.split()
                if len(parts) != 2:
                    conn.send("Usage: %groupusers [group name]".encode())
                    continue
                group_name = parts[1]
                if group_name in groups:
                    if group_name in user_groups:
                        user_list = ', '.join([usernames[c] for c in groups[group_name]['clients']])
                        conn.send(f"Users in group {group_name}: {user_list}".encode())
                    else:
                        conn.send("You are not a member of this group.".encode())
                else:
                    conn.send("Group does not exist.".encode())
            elif data.startswith('%groupleave'):
                parts = data.split()
                if len(parts) != 2:
                    conn.send("Usage: %groupleave [group name]".encode())
                    continue
                group_name = parts[1]
                if group_name in groups:
                    if group_name in user_groups:
                        groups[group_name]['clients'].remove(conn)
                        user_groups.remove(group_name)
                        conn.send(f"You have left group {group_name}.".encode())
                        group_broadcast(f"{username} has left group {group_name}.", conn, group_name)
                    else:
                        conn.send("You are not a member of this group.".encode())
                else:
                    conn.send("Group does not exist.".encode())
            elif data.startswith('%groupmessage'):
                parts = data.split()
                if len(parts) != 3:
                    conn.send("Usage: %groupmessage [group name] [message ID]".encode())
                    continue
                group_name = parts[1]
                if group_name in groups:
                    if group_name in user_groups:
                        msg_id = int(parts[2])
                        group_msgs = groups[group_name]['messages']
                        if 1 <= msg_id <= len(group_msgs):
                            msg = group_msgs[msg_id - 1]
                            msg_content = f"Message {msg['id']} in group {group_name}:\nSender: {msg['sender']}\nDate: {msg['date']}\nSubject: {msg['subject']}\nContent: {msg['content']}"
                            conn.send(msg_content.encode())
                        else:
                            conn.send("Message ID not found.".encode())
                    else:
                        conn.send("You are not a member of this group.".encode())
                else:
                    conn.send("Group does not exist.".encode())
            elif data.startswith('%exit'):
                conn.send('Disconnecting...'.encode())
                remove_client(conn, user_in_public, user_groups)
                break
            else:
                conn.send("Invalid command.".encode())
    except ConnectionResetError:
        remove_client(conn, user_in_public, user_groups)

def broadcast(message, sender_conn, group):
    for client in group:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                remove_client(client, False, set())

def group_broadcast(message, sender_conn, group_name):
    group = groups[group_name]['clients']
    for client in group:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                remove_client(client, False, set())

def remove_client(conn, user_in_public, user_groups):
    username = usernames.get(conn, 'Unknown')
    if conn in usernames:
        del usernames[conn]
    if user_in_public and conn in public_group['clients']:
        public_group['clients'].remove(conn)
        broadcast(f"{username} has left the public message board.", conn, public_group['clients'])
    for group_name in list(user_groups):
        if conn in groups[group_name]['clients']:
            groups[group_name]['clients'].remove(conn)
            group_broadcast(f"{username} has left group {group_name}.", conn, group_name)
    conn.close()
    print(f"{username} has disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server.close()

if __name__ == "__main__":
    start_server()
