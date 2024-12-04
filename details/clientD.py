# client.py

#import socket,threading
import socket
import threading

#listen for messages from server
def receive_messages(sock):
    while True:
        try:
            #receive message from server
            message = sock.recv(1024).decode()
            if message == '':
                print("Disconnected from server.")
                sock.close()
                break
            #print message if not empty
            print(message)
        except:
            break

def main():
    #display welcome message
    print("Welcome to our Bulletin Board of Oz!")
    print("Use %connect to connect to the server.")
    print("Use %help to see available commands.")

    #socket object
    sock = None
    #boolean for connection
    connected = False

    #loop for user commands
    while True:
        command = input()
        
        #%help command to display all available commanbds
        if command.startswith('%help'):
            display_help()  
        
        #%connect command to connect to server
        elif command.startswith('%connect'):
            if connected:
                print("Already connected to a server.")
                continue
            parts = command.split() #split address & port from input, store in list
            if len(parts) != 3:
                print("Usage: %connect [address] [port]")
                continue
            address = parts[1]
            port = int(parts[2]) #convert port input to number for socket
            
            #create tcp/ip socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((address, port)) #connect to specified server
                connected = True #switch boolean once connected
                print("Connected to the server.")

                #start separate thread to listen for incoming messages from server
                receive_thread = threading.Thread(target=receive_messages, args=(sock,))
                receive_thread.daemon = True
                receive_thread.start()

                #username input
                username = input("Enter your username: ")
                sock.send(username.encode())

            except ConnectionRefusedError:
                print("Unable to connect to the server.")
                sock.close()
                sock = None

        #%exit command to disconnect from server       
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



# Python to Java Migration Attempt

# // JavaClient.java
# import java.io.*;
# import java.net.*;
# import java.util.Scanner;

# /*
#  * Incomplete Java client for the bulletin board system.
#  * We started setting up the connection but faced issues and stopped early.
#  */

# public class JavaClient {
#     private Socket socket;
#     private PrintWriter out;
#     private Scanner scanner;

#     public JavaClient() {
#         scanner = new Scanner(System.in);
#     }

#     public void start() {
#         System.out.print("Enter server address: ");
#         String address = scanner.nextLine();
#         System.out.print("Enter server port: ");
#         int port = Integer.parseInt(scanner.nextLine());

#         try {
#             // Attempt to connect to the server
#             socket = new Socket(address, port);
#             System.out.println("Connected to the server.");

#             // Set up output stream
#             out = new PrintWriter(socket.getOutputStream(), true);

#             // We intended to set up input stream and start sending commands
#             // But faced issues with blocking calls and encoding

#             // Decided to stop here due to time constraints and focus on Python client
#         } catch (IOException e) {
#             System.err.println("IOException: " + e.getMessage());
#             // Encountered issues with socket connection, possibly due to server compatibility
#         } finally {
#             // Cleanup resources
#             try {
#                 if (out != null) out.close();
#                 if (socket != null) socket.close();
#                 scanner.close();
#             } catch (IOException e) {
#                 System.err.println("IOException during closing connections: " + e.getMessage());
#             }
#         }
#     }

#     public static void main(String[] args) {
#         JavaClient client = new JavaClient();
#         client.start();
#     }
# }