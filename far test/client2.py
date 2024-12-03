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
        if command.startswith('%connect'):
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
                username = input()
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

if __name__ == "__main__":
    main()
