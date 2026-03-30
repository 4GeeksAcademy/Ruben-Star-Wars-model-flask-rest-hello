import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Date, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()

class MediaTypes(enum.Enum):
    VIDEO = "video"
    IMAGE = "image"


class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    alias: Mapped[str] = mapped_column(String(15), nullable=True)
    biography: Mapped[str] = mapped_column(String(120), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date(), nullable=True)

    posts = relationship("Post", back_populates="users")
    followers = relationship("Follower", back_populates="users")
    comments = relationship("Comment", back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "alias": self.alias,
            "biography": self.biography,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    likes: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)

    #post conecta con user, comment y media
    users = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")
    medias = relationship("Media", back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "likes": self.likes
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    

    #comment conecta con user y post
    users = relationship("User", back_populates="comments")
    posts = relationship("Post", back_populates="posts")


    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Follower(db.Model):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    
    posts = relationship("Post", back_populates="follower")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "follower_id": self.follower_id
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[MediaTypes] = mapped_column(Enum(MediaTypes), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    

    posts = relationship("Media", back_populates="media")

    
    def serialize(self):
        return {
            "id": self.id,
            "media_type": self.media_type.value,
            "url": self.url,
            "post_id": self.post_id
        }