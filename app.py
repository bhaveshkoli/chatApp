from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}

@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    socketio.emit("update_rooms", list(rooms.keys()))




@socketio.on("chat_message")
def handle_chat_message(data):
    username = data["username"]
    message = data["message"]
    room = data["room"]
    
    # Send message to everyone in the room
    socketio.emit("chat_message", {"username": username, "message": message}, room=room)





@socketio.on("create_room")
def handle_create_room(data):
    room = data["room"]
    if room not in rooms:
        rooms[room] = []
        socketio.emit("update_rooms", list(rooms.keys()))  # Send updated room list



@socketio.on("join_room")
def handle_join_room(data):
    username = data["username"]
    room = data["room"]

    if room not in rooms:
        rooms[room] = []
    if username not in rooms[room]:
        rooms[room].append(username)

    join_room(room)
    socketio.emit("update_rooms", list(rooms.keys()))  # Send updated room list
    socketio.emit("chat_message", {"username": "Server", "message": f"{username} joined #{room} room" }, room=room)
    



@socketio.on("leave_room")
def handle_leave_room(data):
    username = data["username"]
    room = data["room"]
    
    if room in rooms and username in rooms[room]:
        rooms[room].remove(username)
        if not rooms[room]:  # Delete room if empty
            del rooms[room]

    leave_room(room)
    socketio.emit("update_rooms", list(rooms.keys()))  # Send updated room list
    socketio.emit("chat_message", {"username": "Server", "message": f"{username} left {room}."}, room=room)








if __name__ == "__main__":
    socketio.run(app,port=8080,  debug=True )
