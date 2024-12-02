import tkinter as tk
import threading

class BulletinBoardClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulletin Board Client")
        self.root.geometry("500x500")

        # Remove the need for client.py
        self.client_socket = None

        self.text_display = tk.Text(root, wrap=tk.WORD, height=15, width=50)
        self.text_display.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        self.send_button = tk.Button(root, text="Send Command", command=self.send_command)
        self.send_button.pack(pady=5)

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

    def connect_to_server(self):
        """Mock server connection (simulate communication)."""
        # Instead of connecting to the real server, we simulate a connection.
        self.client_socket = "MockConnection"
        threading.Thread(target=self.handle_server_messages, daemon=True).start()

    def send_command(self):
        """Simulate sending a command and receiving a response."""
        command = self.entry.get()
        if self.client_socket:
            # Simulate sending a command and getting a response
            response = self.mock_server_response(command)
            self.text_display.insert(tk.END, f"Sent: {command}\nReceived: {response}\n")
            self.text_display.yview(tk.END)  # Scroll to the bottom
        self.entry.delete(0, tk.END)

    def mock_server_response(self, command):
        """Mock server response based on the command sent."""
        # This is just a simple mock that can be extended
        if command.startswith("%groups"):
            return "Available groups: Muchkin, EmeraldCity, YellowBrick, Quadling, Gillikin"
        elif command.startswith("%groupjoin"):
            return f"Joined group: {command.split()[1]}"
        else:
            return f"Unknown command: {command}"

    def handle_server_messages(self):
        """Simulate receiving server messages."""
        # Simulating periodic server responses
        import time
        while True:
            time.sleep(5)
            self.text_display.insert(tk.END, "Server message: Test response\n")
            self.text_display.yview(tk.END)  # Scroll to the bottom

def main():
    root = tk.Tk()
    app = BulletinBoardClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
