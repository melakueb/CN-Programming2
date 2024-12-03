# the tkinter package will be used for the gui
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading

#functions below that will customize the widget and connect to the client.py and server.py code
class BulletinBoardGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bulletin Board")  # Window title
        self.master.geometry("600x400")
        self.sock = None
        self.connected = False
        self.create_widgets()
    
    #widgets for the gui customization
    def create_widgets(self):

        # The connection frame made below
        self.connection_frame = ttk.LabelFrame(self.master, text="Connection")
        self.connection_frame.pack(padx=10, pady=5, fill="x")
        # making and labeling the server ip entry
        self.server_ip_label = ttk.Label(self.connection_frame, text="Server IP:")
        self.server_ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.server_ip_entry = ttk.Entry(self.connection_frame)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.server_ip_entry.grid(row=0, column=1, padx=5, pady=5)
        #making and labeling the port number
        self.server_port_label = ttk.Label(self.connection_frame, text="Port:")
        self.server_port_label.grid(row=1, column=0, padx=5, pady=5)
        self.server_port_entry = ttk.Entry(self.connection_frame)
        self.server_port_entry.insert(0, "65432")
        self.server_port_entry.grid(row=1, column=1, padx=5, pady=5)
        #making and labeling the connect button that will connect to the server using the port and server number
        self.connect_button = ttk.Button(self.connection_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5)
        self.disconnect_button = ttk.Button(self.connection_frame, text="Disconnect", command=self.disconnect_from_server)
        self.disconnect_button.grid(row=0, column=3, rowspan=2, padx=5, pady=5)
        self.disconnect_button.config(state=tk.DISABLED)
        # The frame for the command input is made
        self.command_frame = ttk.LabelFrame(self.master, text="Command Input")
        self.command_frame.pack(padx=10, pady=5, fill="x")
        self.command_entry = ttk.Entry(self.command_frame)
        self.command_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
        self.command_entry.bind('<Return>', lambda event: self.send_command())
        # Send button code here
        self.send_button = ttk.Button(self.command_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)
        # Button for the help button that will show all commands using show_commands
        self.help_button = ttk.Button(self.master, text="Help", command=self.show_commands)
        self.help_button.pack(padx=10, pady=5)
        # Frame for "Display" where all the messages and inputs will be shown
        self.message_frame = ttk.LabelFrame(self.master, text="Display")
        self.message_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.message_display = scrolledtext.ScrolledText(self.message_frame, state='disabled', wrap='word')
        self.message_display.pack(padx=5, pady=5, fill="both", expand=True)

   #Function for the connection to the server
    def connect_to_server(self):
        if self.connected:
            self.update_display("Already connected to a server.")
            return
        try:
            # Will get the server ip and port entry and connect to the server
            address = self.server_ip_entry.get()
            port = int(self.server_port_entry.get())
            # Code for the socket. this will allow a connection between the client and server 
            # and for messages to be passed through
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((address, port))
            self.connected = True
            self.update_display(f"Connected to {address}:{port}")
            self.disconnect_button.config(state=tk.NORMAL)
            self.connect_button.config(state=tk.DISABLED)
            # Thi code will allow receiving messages in a separate thread
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.update_display(f"Error: {e}")
            self.connected = False
   
    # Disconnect function that will disconnect from the server 
    # which will be executed through the disconnect button in the gui
    def disconnect_from_server(self):
        if self.connected:
            self.sock.send("%exit".encode())
            self.sock.close()
            self.connected = False
            self.update_display("Disconnected from the server.")
            self.disconnect_button.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.NORMAL)

    #Function that send the command inputted in the gui
    def send_command(self):
        command = self.command_entry.get()
        if self.connected and command.strip():
            self.sock.send(command.encode())
            if command == "%exit":
                self.disconnect_from_server()
            self.command_entry.delete(0, tk.END)
        #error message if command doesn't exist
        else:
            self.update_display("Not connected to a server or empty command.")

#Function to receive messages and push them on display widget
    def receive_messages(self):
        while self.connected:
            try:
                message = self.sock.recv(1024).decode()
                if not message:
                    self.disconnect_from_server()
                    break
                self.update_display(message)
            except:
                self.disconnect_from_server()
                break

#Funtion to update display 
    def update_display(self, message):
        self.message_display.config(state='normal')
        self.message_display.insert(tk.END, message + "\n")
        self.message_display.config(state='disabled')
        self.message_display.see(tk.END)
#Functions to get and all commands that can be used
    def show_commands(self):
        commands = self.get_command_list()
        self.update_display(commands)
    def get_command_list(self):
        # List of available commands with a description
        return (
            "%connect [IP] [port] - Connect to the server\n"
            "%join - Join the message board\n"
            "%post [subject] [message] - Post a message\n"
            "%users - List users in the group\n"
            "%leave - Leave the group\n"
            "%message [ID] - Retrieve a message by ID\n"
            "%exit - Disconnect from the server\n"
            "%groups - List available groups\n"
            "%groupjoin [group] - Join a specific group\n"
            "%grouppost [group] [subject] [message] - Post a message to a group\n"
            "%groupusers [group] - List users in a group\n"
            "%groupleave [group] - Leave a group\n"
            "%groupmessage [group] [ID] - Retrieve a message from a group"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BulletinBoardGUI(root)
    root.mainloop()
