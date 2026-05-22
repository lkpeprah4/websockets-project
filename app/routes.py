from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Room, Message

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms", methods=["POST"])
def create_room():
    data=request.get_json()
    name=data.get("name")

    if not name:
        return jsonify ({"error":"ROOM NAME IS REQUIRED"}),400
    
    existing_room = Room.query.filter_by(name=name).first()
    if existing_room:
        return jsonify({"error": "Room already exists"}), 400

    room = Room(name=name)
    db.session.add(room)
    db.session.commit()

    return jsonify({"msg":"ROOM CREATED SUCESSFULLY","room":room.to_dict()}), 201


@rooms_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms=Room.query.all()
    return jsonify({"rooms":[room.to_dict() for room in rooms]}),200


@rooms_bp.route("/rooms/<string:name>/messages", methods=["GET"])
def get_messages(name):
    room=Room.query.filter_by(name=name).first()

    if not room:
        return jsonify({"msg":"ROOM NOT FOUND"}),404
    
    messages=Message.query.filter_by(room_id=room.id).all()
    return jsonify({"messages":[message.to_dict() for message in messages]}),200
