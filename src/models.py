from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey  # <--- Agrega ForeignKey aquí
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    firstname: Mapped[str] = mapped_column(String(25))
    lastname: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
   
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.username,
            "lastname": self.username,
            "email": self.email,
            "username": self.username,    
        }

class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"),primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"),primary_key=True)
   
   
    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,  
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
   
    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id, 
        } 
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(25))
    url: Mapped[str] = mapped_column(String(150))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id, 
        } 