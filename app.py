from web_socket_server import WebSocketServer, socketio, app
from flask import render_template

app = WebSocketServer().create_app()
# Hashmap
message_storage = {}

@socketio.on('connect')
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

# Updated Message Event
@socketio.on('message')
def handle_message(data):
    # Setting author and message
    author = data.get('author')
    message = data.get('message')
    print(f'Message received from {author}: {message}')

    if not author or not message:
        print("Invalid data received")
        return

    # If author not in hashmap, add the author to the hashmap
    if author not in message_storage:
        message_storage[author] = []

    message_storage[author].append(message)

    # Emit message to all connected users
    socketio.emit('message', {"author": author, "message": message})

# Get all user messages
@socketio.on('get_user_messages')
def handle_get_user_messages(data):
    author = data.get('author')

    # If data is not author
    if not author:
        print("Invalid data recieved")
        return
    
    # Get author and its messages
    user_messages = message_storage.get(author, [])
    socketio.emit('get_user_messages', {"author": author, "messages": user_messages})

# Edit a message that a user has sent
@socketio.on('edit_message')
def handle_edit_message(data):
    author = data.get('author')
    old_message = data.get('old_message')
    new_message = data.get('new_message')

    if not author or not old_message or not new_message:
        return

    # Edit message in storage
    if author in message_storage and old_message in message_storage[author]:
        index = message_storage[author].index(old_message)
        message_storage[author][index] = new_message

        # Emit updated message
        socketio.emit('edit_message', {"author": author, "old_message": old_message, "new_message": new_message})

# Delete a message that a author has sent
@socketio.on('delete_message')
def handle_delete_message(data):
    author = data.get('author')
    message = data.get('message')

    if not author or not message:
        return

    # Delete the message from storage
    if author in message_storage and message in message_storage[author]:
        message_storage[author].remove(message)

        # Emit deleted message info
        socketio.emit('delete_message', {"author": author, "message": message})

# Landing Page
@app.route('/')
def index():
    return render_template('WebSocketClient.html')

# Link to chatroom1
@app.route('/chatroom1')
def chatroom1():
    return render_template('ChatRoom1.html')

# Link to chatroom2
@app.route('/chatroom2')
def chatroom2():
    return render_template('ChatRoom2.html')

if __name__ == '__main__':
    socketio.run(app)