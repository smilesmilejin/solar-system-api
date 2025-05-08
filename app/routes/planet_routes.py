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
from app.models.moon import Moon
from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.routes.route_utilities import validate_model, create_model

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")


@planets_bp.post("")
def create_planet():
    request_body = request.get_json()

    # ###### 2
    # ############## 1
    # # name = request_body['name']
    # # description = request_body['description']
    # # size = request_body['size']
    # # new_planet = Planet(name=name, description=description, size=size)

    # ############## 1
    # new_planet = Planet.from_dict(request_body)

    # db.session.add(new_planet)
    # db.session.commit()

    # # response = {
    # #     "id": new_planet.id,
    # #     "name": new_planet.name,
    # #     "description": new_planet.description,
    # #     "size": new_planet.size
    # # }

    # # return response, 201

    # return new_planet.to_dict(), 201
    # ###### 2
    return create_model(Planet, request_body)

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

        ################## 1 
        # planets_response.append(
        #     planet.to_dict()
        #     # {
        #     #     "id": planet.id,
        #     #     "name": planet.name,
        #     #     "description": planet.description,
        #     #     "size": planet.size      
        #     # }
        # )
         ################## 1 

        # Wave 8 
        # If the planet has moons, add them to the reponse
        planet_dict = planet.to_dict()
        if planet.moons:
            planet_dict["moons"]= [moon.to_dict() for moon in planet.moons]
        
        planets_response.append(planet_dict)

    return planets_response


# Wave 4
@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    # planet = validate_planet(planet_id)
    planet = validate_model(Planet, planet_id)
    
    return planet.to_dict()
    # return {
    #     "id": planet.id,
    #     "name": planet.name,
    #     "description": planet.description,
    #     "size": planet.size
    # }

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    # planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.size = request_body["size"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         invalid = {'message': f"Planet id ({planet_id}) is invalid."}
#         abort(make_response(invalid, 400))
    
#     query = db.select(Planet).where(Planet.id == planet_id)
#     planet = db.session.scalar(query)
    
#     if not planet:
#         not_found = {'message': f"Planet with id ({planet_id}) not found."}
#         abort(make_response(not_found, 404))

#     return planet

# Wave 8 
# ●	Add nested routes for the endpoint `/planets/<planet_id>/moons` to:
# ○	Create a Moon and link it to an existing Planet record
# ○	Fetch all Moons that a Planet is associated with

# ●	Create a nested route for `/planets/<planet_id>/moons` 
# with the POST method which allows you to add a new moon to an existing planet 
# resource with id `<planet_id>`.

@planets_bp.post("/<planet_id>/moons")
def create_moon_with_planet_id(planet_id):
    # Validate planet_id 
    planet = validate_model(Planet, planet_id)

    # request body will be moon (name, description, size)
    request_body = request.get_json()
    #int(planet_id)
    request_body["planet_id"] = planet.id

    # ###### 2
    # try:
    #     new_moon = Moon.from_dict(request_body)
    # except KeyError as e:
    #     response = {"message": f"Invalid request: missing {e.args[0]}"}
    #     abort(make_response(response, 400))

    # db.session.add(new_moon)
    # db.session.commit()

    # response = new_moon.to_dict()

    # ###### 2
    response = create_model(Moon, request_body)[0]

    # Moved this to moon to_dict()
    # # Add planet id and name to the moon response
    # response["planet_id"] = planet.id
    # response["planet"] = planet.name

    return response, 201


# ●	Create a nested route for `/planets/<planet_id>/moons` 
# with the GET method which returns all moons for the planet with the id `<planet_id>`.
@planets_bp.get("/<planet_id>/moons")
def get_moons_by_planet_id(planet_id):
    planet = validate_model(Planet, planet_id)
    moons = [moon.to_dict() for moon in planet.moons]

    # print(planet.moons) # [<Moon 1>, <Moon 2>]
    return moons