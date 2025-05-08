# # Wave 01: Setup and Read
# class Planet:
#     def __init__(self, id, name, description, size):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.size = size


# planets = [
#     Planet(1, "Mercury", "The smallest planet in the solar system", 4880),
#     Planet(2, "Jupiter", "The larges planet in the solar system", 43400),
#     Planet(3, "Venus", "Similar in size to Earth", 12104),
#     Planet(4, "Mars", "Smaller terrestrial Planets", 6779)
# ]

# Wave 3
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    size: Mapped[int]

    # Planet table:
    # One-to-many: One planet has many moons
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "size": self.size

            # Add moons
            # "moons": [moon.to_dict() for moon in self.moons]
        }
    
    @classmethod
    def from_dict(cls, planet_data):
        return cls(
            name=planet_data["name"],
            description=planet_data["description"],
            size=planet_data["size"]
        )

