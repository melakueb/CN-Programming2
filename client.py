#import socket
import socket
# Define server details
SERVER = '127.0.0.1'
PORT = 3000

# group names
available_groups = ['Muchkin', 'EmeraldCity', 'YellowBrick', 'Quadling', 'Gillikin']
active_group = None
joined_groups = []

def print_commands():
    """Print all available commands and their usage."""
    print("\nAvailable Commands:")
    print("%groups              - List all available groups.")
    print("%groupjoin <group>   - Join a specific group by name.")
    print("%post <message>      - Post a message to the public board.")
    print("%users               - Retrieve a list of users in your current group.")
    print("%groupusers <group>  - Retrieve a list of users in a specific group.")
    print("%grouppost <group> <message> - Post a message to a specific group.")
    print("%groupmessage <group> <id>   - Retrieve a specific message from a group by ID.")
    print("%groupleave <group>  - Leave a specific group.")
    print("%leave               - Exit all groups and disconnect.")
    print("\nType a command to get started.\n")

def start_client():
    # initialize client socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # estbalish connection to the server
    print("Connecting to the server...")
    client_socket.connect((SERVER, PORT))
    print("Connected to the server.")

    # Receive welcome message
    print_commands()

    # messages loop
    while True:
        # receive messages from the server
        response = client_socket.recv(1024).decode('utf-8')
        if not response:
            print("Server disconnected. Exiting...")
            client_socket.close()
            break
        print(response.strip())

    
#prompt with all commands

        # user input for commands
        user_input = input("Enter -> ")
        client_socket.sendall(user_input.encode('utf-8'))


        if user_input.startswith("%groups"):
            #show the list of group names
            for group in available_groups:
                print(f"- {group}")            
            client_socket.sendall("%groups".encode('utf-8'))

        elif user_input.startswith("%groupjoin"):
            # Join a group and add to the group list
            group_name = user_input.split()[1]
            if group_name in available_groups:
                if group_name not in joined_groups:
                    joined_groups.append(group_name)
                    print(f"Joined group: {group_name}")
                else:
                    print(f"You have already joined {group_name}.")
                active_group = group_name
                client_socket.sendall(f"%groupjoin {group_name}".encode('utf-8'))

                # Wait for server confirmation
                try:
                    response = client_socket.recv(1024).decode('utf-8')
                    print(response.strip())
                except Exception as e:
                    print(f"Error receiving response for %groupjoin: {e}")
            else:
                print("Invalid group name.")


        elif user_input.startswith("%post"):
            #post a messafe
            if active_group:
                # **Part 2: Post Message in Private Group**
                client_socket.sendall(f"%grouppost {active_group} {user_input[6:]}".encode('utf-8'))
            else:
                # **Part 1: Post Message to Public Board**
                client_socket.sendall(user_input.encode('utf-8'))

        elif user_input.startswith("%users"):
            args = user_input.split()
            if len(args) > 1 and args[1] in joined_groups:
                # Part 2: Get Users in a specific Private Group
                client_socket.sendall(f"%groupusers {args[1]}".encode('utf-8'))
            elif len(args) == 1:
                # Part 1: Get Users in Public Group
                client_socket.sendall("%users".encode('utf-8'))
            else:
                print("You are not a member of this group.")

        elif user_input.startswith("%message"):
            if active_group:
                # **Part 2: Get Message from Private Group**
                client_socket.sendall(f"%groupmessage {active_group} {user_input[9:]}".encode('utf-8'))
            else:
                # **Part 1: Get Message from Public Board**
                client_socket.sendall(user_input.encode('utf-8'))

        elif user_input.startswith("%groupleave"):
            group_name = user_input.split()[1]
            if group_name in joined_groups:
                joined_groups.remove(group_name)
                if active_group == group_name:
                    active_group = None
                print(f"You have left the group: {group_name}")
                client_socket.sendall(f"%groupleave {group_name}".encode('utf-8'))
            else:
                print("You are not a member of this group.")

        elif user_input.startswith("%leave"):
            print("Exiting the group...")
            if active_group:
                # **Part 2: Leave Private Group**
                client_socket.sendall(f"%groupleave {active_group}".encode('utf-8'))
                active_group = None
            client_socket.close()
            break

if __name__ == "__main__":
    start_client()




# import socket

# SERVER = '127.0.0.1'
# PORT = 3000

# available_groups = ['Muchkin', 'EmeraldCity', 'YellowBrick', 'Quadling', 'Gillikin']
# active_group = None
# joined_groups = []

# def start_client():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print("Connecting to the server...")
#     client_socket.connect((SERVER, PORT))
#     print("Connected to the server.")

#     # Get initial server prompt and send username
#     username_prompt = client_socket.recv(1024).decode()
#     print(username_prompt, end='')
#     username = input()
#     client_socket.send(username.encode())

#     # Get welcome message
#     welcome = client_socket.recv(1024).decode()
#     print(welcome)

#     while True:
#         user_input = input("Enter -> ")
#         if not user_input:
#             continue

#         client_socket.send(user_input.encode())

#         if user_input.startswith("%groups"):
#             for group in available_groups:
#                 print(f"- {group}")

#         elif user_input.startswith("%groupjoin"):
#             group_name = user_input.split()[1]
#             if group_name in available_groups and group_name not in joined_groups:
#                 joined_groups.append(group_name)
#                 active_group = group_name

#         elif user_input.startswith("%groupleave"):
#             group_name = user_input.split()[1]
#             if group_name in joined_groups:
#                 joined_groups.remove(group_name)
#                 if active_group == group_name:
#                     active_group = None

#         elif user_input == "%leave":
#             print("Disconnecting...")
#             break

#         # Get server response
#         response = client_socket.recv(1024).decode()
#         if not response:
#             break
#         print(response)

#     client_socket.close()

# if __name__ == "__main__":
#     start_client()