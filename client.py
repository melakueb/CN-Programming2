import socket

# Server details
SERVER = '127.0.0.1'
PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    try:
        while True:
            # Receive messages from server
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                break
            print(response.strip())

            # Take user input and send to server
            user_input = input("> ")
            client_socket.sendall(user_input.encode('utf-8'))
            if user_input.startswith("%leave"):
                print("Exiting the group...")
                break
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
