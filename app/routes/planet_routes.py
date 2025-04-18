from app.models.planet import planets
from flask import Blueprint, abort, make_response

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")


# Wave 1
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

# Wave 2
@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    planet_dict = (dict(
        id = planet_id,
        name = planet.name,
        description = planet.description,
        size = planet.size)
    )
    
    return planet_dict

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        invalid = {"message": f"Planet id ({planet_id}) is invalid."}
        abort(make_response(invalid, 400))

    for planet in planets:
        if planet.id == planet_id:
            return planet
    
    not_found = {"message": f"Planet_id ({planet_id}) not found"}
    abort(make_response(not_found, 404))



