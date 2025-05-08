from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional

# one-to-many relationship: One planet could have many moons
# some moon does not have planet
class Moon(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    size: Mapped[int]
    
    # One moon has 0 to 1 moon
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moons")

    # Planet is the model name
    # moons is the attribute of the another model
    # Planet table:
    # moons: Mapped[list["Moon"]] = relationship(back_populates="planet")


    # ####### Example

    # # One caretaker could have many cats
    # # caretaker table
    # cats: Mapped[list["Cat"]] = relationship(back_populates="caretaker")

    # # cat table
    # caretaker_id: Mapped[Optional[int]] = mapped_column(ForeignKey("caretaker.id"))
    # caretaker: Mapped[Optional["Caretaker"]] = relationship(back_populates="cats")


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "size": self.size,
            "planet_id": self.planet_id if self.planet_id else None,
            "planet": self.planet.name if self.planet_id else None
        }
    
    @classmethod
    def from_dict(cls, moon_data):
        return cls(
            name=moon_data["name"],
            description=moon_data["description"],
            size=moon_data["size"],
            planet_id=moon_data.get("planet_id", None)
        )