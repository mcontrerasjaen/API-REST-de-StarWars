from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String(20)) # Subí a 20 por seguridad
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    height: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "description": self.description,
            "hair_color": self.hair_color
        }

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    climate: Mapped[str] = mapped_column(String(20))
    population: Mapped[str] = mapped_column(String(20))
    diameter: Mapped[str] = mapped_column(String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "diameter": self.diameter
        }

class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planetas.id"))
    people_id: Mapped[Optional[int]] = mapped_column(ForeignKey("personajes.id"))
  
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }