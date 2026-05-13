from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__= "books"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    created_at=db.Column(db.DateTime(),default=datetime.utcnow,nullable=False)
    author=db.Column(db.String(200),nullable=False)

    reviews=db.Relationship("Review", backref="book", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "created_at": self.created_at.isoformat()
        }
 

class Review(db.Model):
    __tablename__= "review"
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    rating=db.Column(db.Integer ,nullable=False)
    username=db.Column(db.String(50),nullable=False)
    book_id=db.Column(db.ForeignKey("books.id"))

    def to_dict(self):
        return{
            "id":self.id,
            "content":self.content,
            "rating":self.rating,
            "username":self.rating,
            "book_id":self.book_id,
            "created_at":self.created_at.isoformat()
        }


