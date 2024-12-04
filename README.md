# **Simple Bulletin Board System**
#### By: Elshaddai, Ikran, Fareena

## **Overview**

This project implements a simple bulletin board system using socket programming in Python. It consists of a server and a client that allow users to:

- Connect to the server.
- Join a public message board.
- Post and retrieve messages.
- Join multiple private groups.
- Communicate with other users in real-time.

---

## **Commands**


### **General Commands**

- **%connect [address] [port]**: Connects to the bulletin board server at the specified address and port.

- **%exit**: Disconnects from the server and exits the client program.

### **Public Message Board Commands**

- **%join**: Joins the public message board where all users can interact.

- **%post [subject] [content]**: Posts a message with the given subject and content to the public message board.

- **%message [message ID]**: Retrieves the full content of the specified message from the public board.

- **%users**: Displays a list of users currently in the public message board.

- **%leave**: Leaves the public message board.

### **Private Group Commands**

- **%groups**: Retrieves a list of all available groups that can be joined.

- **%groupjoin [group name]**: Joins the specified group.

- **%grouppost [group name] [subject] [content]**: Posts a message with the given subject and content to the specified group.

- **%groupmessage [group name] [message ID]**: Retrieves the full content of the specified message from the given group.

- **%groupusers [group name]**: Displays a list of users currently in the specified group.

- **%groupleave [group name]**: Leaves the specified group.

### **How to Navigate the GUI**
1) Enter the server and host you want to connect to. Then click connect.
2) Follow the prompt in the display to enter your username in the Command input entry.
3) Use any commands you wish. If you need help with any commands, click on the help button and it will print a list of commands you can use. NOTE: you have to be a user in order to use the help button. So, enter your username first, then use the help button. 


### **Major Issues Encountered**
As we completed this project, we ran into some issues that served as barriers that have since been resolved. These include:
1) Active Groups
-- Issue: Initially, we attempted to track all groups a user joined and determine the "active group" for posting based on the most recent group. This approach was not working well.
-- Resolution: The current implementation eliminates the need for an "active group" by requiring users to specify the group name explicitly when posting (e.g., %grouppost [group name] [subject] [content]). This ensures clarity and allows users to interact with multiple groups without ambiguity.

2) Handling Connections
-- Issue: The server initially struggled to recognize when users disconnected
-- Resolution: The remove_client function now reliably removes users from all groups upon disconnection and notifies others. Improved error handling ensures that lingering connections are cleaned up effectively.

3) Message ID Assignment
-- Issue: Message IDs were incorrectly assigned, which made message retrieval unreliable.
-- Resolution: IDs are now assigned sequentially based on the length of the messages list in each group, ensuring unique and consistent message tracking.

