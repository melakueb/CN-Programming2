# import socket
# import threading

# def receive_messages(client_socket):
#     """Receives and prints messages from the server."""
#     while True:
#         try:
#             message = client_socket.recv(1024).decode()
#             print(message)
#         except:
#             print("Disconnected from server.")
#             break

# def main():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(("127.0.0.1", 12345))

#     threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

#     while True:
#         try:
#             command = input("> ")
#             client_socket.sendall(command.encode())
#             if command == "%leave" or command == "%exit":
#                 break
#         except:
#             print("Connection lost.")
#             break

#     client_socket.close()

# if __name__ == "__main__":
#     main()


# claude below

import socket

# Server configuration
HOST = 'localhost'
PORT = 12345

def send_command(command):
    client_socket.send(command.encode())
    response = client_socket.recv(1024).decode()
    print(response)

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to the server.")

while True:
    command = input("Enter a command: ")
    
    if command.startswith('%connect'):
        send_command(command)
    
    elif command == '%join':
        send_command(command)
    
    elif command.startswith('%post'):
        send_command(command)
    
    elif command == '%users':
        send_command(command)
    
    elif command == '%leave':
        send_command(command)
    
    elif command.startswith('%message'):
        send_command(command)
    
    elif command == '%exit':
        send_command(command)
        break
    
    elif command == '%groups':
        send_command(command)
    
    elif command.startswith('%groupjoin'):
        send_command(command)
    
    elif command.startswith('%grouppost'):
        send_command(command)
    
    elif command.startswith('%groupusers'):
        send_command(command)
    
    elif command.startswith('%groupleave'):
        send_command(command)
    
    elif command.startswith('%groupmessage'):
        send_command(command)
    
    else:
        print("Invalid command.")

client_socket.close()