from app.extensions import db
from datetime import datetime

class Room(db.Model):
    __tablename__="rooms"

    id= db.Column(db.Integer ,primary_key=True)
    name=db.Column(db.String, unique=True ,nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    messages=db.relationship("Message", backref="room", lazy=True)
    def to_dict(self):
        return{
            "id": self.id,
            "name":self.name,
            "created_at":self.created_at.isoformat()
        }


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_username = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "sender_username": self.sender_username,
            "room_id": self.room_id,
            "created_at": self.created_at.isoformat()
        }