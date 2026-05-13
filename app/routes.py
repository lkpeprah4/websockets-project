from flask import Blueprint, request
from app.extensions import db
from app.models import Room, Message

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("rooms", methods=["POST"])
def create_room():
    data=request.get_json()

    if not data or no