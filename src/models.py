import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Date, Integer, Float, ForeignKey, Enum
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
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    date_of_suscription: Mapped[date] = mapped_column(Date(), nullable=False)

    favorite_planets = relationship("Favorite_planet", back_populates="users")
    favorite_characters = relationship("Favorite_character", back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "date_of_suscription": self.date_of_suscription.isoformat() if self.date_of_suscription else None
        }


class Planet(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    population: Mapped[int] = mapped_column(
        Integer(), nullable=False, default=0)
    diameter: Mapped[float] = mapped_column(Float(), nullable=False)

    favorite_planets = relationship("Favorite_planet", back_populates="planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter
        }


class Character(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    height: Mapped[int] = mapped_column(Integer(), nullable=False)
    mass: Mapped[int] = mapped_column(Integer(), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(15), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(15), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date(), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)

    favorite_characters = relationship("Favorite_planet", back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "birth_date": self.birth_date,
            "gender": self.gender
        }


class Favorite_character(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("character.id", ondelete="CASCADE"), nullable=False)

    users = relationship("User", back_populates="favorite_characters")
    characters = relationship("Character", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }


class Favorite_planet(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("planet.id", ondelete="CASCADE"), nullable=False)

    users = relationship("User", back_populates="favorite_planets")
    planets = relationship("Planet", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
