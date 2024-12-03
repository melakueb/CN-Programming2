# client.py
import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message == '':
                print("Disconnected from server.")
                sock.close()
                break
            print(message)
        except:
            print("Disconnected from server.")
            sock.close()
            break

def main():
    sock = None
    connected = False
    while True:
        command = input()
        if command.startswith('%help'):
            display_help()  # Display available commands
        elif command.startswith('%connect'):
            if connected:
                print("Already connected to a server.")
                continue
            parts = command.split()
            if len(parts) != 3:
                print("Usage: %connect [address] [port]")
                continue
            address = parts[1]
            port = int(parts[2])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((address, port))
                connected = True
                print("Connected to the server.")
                receive_thread = threading.Thread(target=receive_messages, args=(sock,))
                receive_thread.daemon = True
                receive_thread.start()
                # Handle username input
                username = input("Enter your username: ")
                sock.send(username.encode())
            except ConnectionRefusedError:
                print("Unable to connect to the server.")
                sock.close()
                sock = None
        elif command.startswith('%exit'):
            if connected:
                sock.send(command.encode())
                sock.close()
                connected = False
                print("Disconnected from the server.")
            else:
                print("You are not connected to any server.")
            break
        else:
            if not connected:
                print("You are not connected to any server. Use %connect to connect.")
                continue
            else:
                # Send command to server
                sock.send(command.encode())
                if command.startswith('%exit'):
                    connected = False
                    break

def display_help():
    """Display available commands."""
    print("""
Available Commands:
%connect [address] [port]  - Connect to the server.
%join                      - Join the public message board.
%post [subject] [content]  - Post a message to the public board.
%users                     - List users in the public message board.
%message [message ID]      - Retrieve a specific message by ID.
%leave                     - Leave the public message board.
%groups                    - List all available private groups.
%groupjoin [group name]    - Join a private group.
%grouppost [group name] [subject] [content] - Post a message to a private group.
%groupusers [group name]   - List users in a specific group.
%groupleave [group name]   - Leave a specific private group.
%groupmessage [group name] [message ID] - Retrieve a message by ID in a private group.
%exit                      - Disconnect from the server and exit.
%help                      - Display this help message.
""")



if __name__ == "__main__":
    main()
