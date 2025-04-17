from app.models.planet import planets
from flask import Blueprint

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

@planets_bp.get("/")

def get_all_planets():
    results_list = []
    for planet in planets:
        results_list.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description":planet.description,
                "size":planet.size

            }
        )

    return results_list