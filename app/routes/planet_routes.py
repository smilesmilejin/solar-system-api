# from app.models.planet import planets
# from flask import Blueprint, abort, make_response

# planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")


# # Wave 1
# @planets_bp.get("/")
# def get_all_planets():
#     results_list = []
    
#     for planet in planets:
#         results_list.append(
#             {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description":planet.description,
#                 "size":planet.size

#             }
#         )

#     return results_list

# # Wave 2
# @planets_bp.get("/<planet_id>")
# def get_one_planet(planet_id):
#     planet = validate_planet(planet_id)

#     planet_dict = (dict(
#         id=planet_id,
#         name=planet.name,
#         description=planet.description,
#         size=planet.size)
#     )
    
#     return planet_dict

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         invalid = {"message": f"Planet id ({planet_id}) is invalid."}
#         abort(make_response(invalid, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
    
#     not_found = {"message": f"Planet_id ({planet_id}) not found"}
#     abort(make_response(not_found, 404))

# Wave 3
from app.models.planet import Planet
from flask import Blueprint, abort, make_response, request, Response
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")


@planets_bp.post("")
def create_planet():
    request_body = request.get_json()

    name = request_body['name']
    description = request_body['description']
    size = request_body['size']

    new_planet = Planet(name=name, description=description, size=size)

    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "size": new_planet.size
    }

    return response, 201

@planets_bp.get("")
def get_all_planets():
    # Wave 5
    query = db.select(Planet)
    
    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name == name_param)
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))
    
    query = query.order_by(Planet.id)
    # query = db.select(Planet).order_by(Planet.id)
    # End Wave 5

    planets = db.session.scalars(query)

    planets_response = []

    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "size": planet.size      
            }
        )
    return planets_response


# Wave 4
@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "size": planet.size
    }

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.size = request_body["size"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        invalid = {'message': f"Planet id ({planet_id}) is invalid."}
        abort(make_response(invalid, 400))
    
    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)
    
    if not planet:
        not_found = {'message': f"Planet with id ({planet_id}) not found."}
        abort(make_response(not_found, 404))

    return planet