# **Bulletin Board System**
### Group: Elshaddai, Ikran, Fareena
---
## **Overview**
This is a program for a bulletin board where users can join, post messages, see other users, and leave the group. It uses Python and basic socket programming for networking.

---

## **How to Run**

### **Server**
1. Run in the terminal:
   ```bash
   python3 bulletin_server.py
   ```

### **Client**
1. Run in the terminal:
   ```bash
   python3 bulletin_client.py
   ```
3. Enter a unique username and follow the prompts.

---

---

## **Commands**

### **Public Message Board Commands (Part 1)**:
- **`%post <message>`**: Posts a message to the public group.
- **`%users`**: Requests the list of users currently in the public group.
- **`%message <ID>`**: Retrieves a specific message by its ID (like asking for an older post).
- **`%leave`**: Exits the group and disconnects the user from the server.

### **Private Group Commands (Part 2)**:
- **`%groups`**: Lists the available private groups the user can join.
- **`%groupjoin <group_name>`**: Joins a specific private group .
- **`%groupleave`**: Leaves the current private group the user is in.

## **Example**
1. Join with a username.
2. Post messages:
   ```
   %post Hello, everyone!
   ```
3. See all connected users:
   ```
   %users
   ```
4. Retrieve a specific message:
   ```
   %message 1
   ```
5. Leave the group:
   ```
   %leave
   ```

# things to add to frontend
- list of active users
- list of cmds + what they mean
