from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio, db
from app.models import Message, Room

# Track active users in each room (in memory)
active_users = {}


@socketio.on("join")
def handle_join(data):
    username = data.get("username")
    room_name = data.get("room")

    if not username or not room_name:
        emit("error", {"msg": "USERNAME AND ROOM ARE REQUIRED"})
        return

    join_room(room_name)

    if room_name not in active_users:
        active_users[room_name] = []
    if username not in active_users[room_name]:
        active_users[room_name].append(username)

    emit("user_joined", {
        "username": username,
        "active_users": active_users[room_name]
    }, room=room_name)


@socketio.on("leave")
def handle_leave(data):
    username = data.get("username")
    room_name = data.get("room")

    if not username or not room_name:
        return

    leave_room(room_name)

    if room_name in active_users and username in active_users[room_name]:
        active_users[room_name].remove(username)


    emit("user_left", {
        "username": username,
        "active_users": active_users[room_name]
    }, room=room_name)


@socketio.on("send_message")
def handle_send_message(data):
    username = data.get("username")
    room_name = data.get("room")
    content = data.get("content")

    if not username or not room_name or not content:
        emit("error", {"msg": "USERNAME, ROOM, AND CONTENT ARE REQUIRED"})
        return

    room = Room.query.filter_by(name=room_name).first()
    if not room:
        emit("error", {"msg": "ROOM NOT FOUND"})
        return


    message = Message(
        content=content,
        sender_username=username,
        room_id=room.id
    )
    db.session.add(message)
    db.session.commit()

    emit("new_message", message.to_dict(), room=room_name)


@socketio.on("react")
def handle_react(data):
    username = data.get("username")
    room_name = data.get("room")
    emoji = data.get("emoji")

    if not username or not room_name or not emoji:
        return

    emit("new_reaction", {
        "username": username,
        "emoji": emoji
    }, room=room_name)