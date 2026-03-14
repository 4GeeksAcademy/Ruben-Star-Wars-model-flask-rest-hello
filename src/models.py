import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Date, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
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

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "alias": self.alias,
            "biography": self.biography,
            "date_of_birth": self.date_of_birth
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("User.id"), nullable=False)
    likes: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "likes": self.likes
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("User.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("Post.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


class Follower(db.Model):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"), primary_key=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "follower_id": self.follower_id
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[MediaTypes] = mapped_column(Enum(), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("Post.id"), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "media_type": self.media_type,
            "url": self.url,
            "post_id": self.post_id
        }