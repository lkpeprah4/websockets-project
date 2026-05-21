from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Room, Message

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms", methods=["POST"])
def create_room():
    data=request.get_json()

    if not data or not data.get("name"):
        return jsonify ({"error":"ROOM NAME IS REQUIRED"}),400
    
    existing_room = Room.query.filter_by(name=data["name"]).first()
    if existing_room:
        return jsonify({"error": "Room already exists"}), 400

    room = Room(name=data["name"])
    db.session.add(room)
    db.session.commit()

    return jsonify(room.to_dict()), 201
    