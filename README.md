# **Bulletin Board System**
### Group: Elshaddai, Ikran, Fareena
---
## **Overview**
This is a program for a bulletin board where users can join, post messages, see other users, and leave the group. It uses Python and basic socket programming.

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

## **Commands**
- **Post a message**: `%post <message>`
- **See users**: `%users`
- **Get a message by ID**: `%message <ID>`
- **Leave the group**: `%leave`

---

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

