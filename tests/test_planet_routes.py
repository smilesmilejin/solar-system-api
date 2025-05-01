# Wave 6
from app.db import db
from app.models.planet import Planet

# Create a test to check GET /planets returns 200 and an empty array.
def test_get_all_planet_returns_empty_list_when_db_is_empty(client):
    response = client.get("/planets")

    assert response.status_code == 200
    assert response.get_json() == []

# 1. GET /planets/1 returns a response body that matches our fixture
def test_get_one_planet(client, one_planet):
    response = client.get("/planets/1")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == one_planet.id
    assert response_body["name"] == one_planet.name
    assert response_body["description"] == one_planet.description
    assert response_body["size"] == one_planet.size

    # Or use this assert 
    assert response_body == {
        "id": 1,
        "name": "Earth",
        "description": "Earth is the third planet from the Sun ",
        "size": 12742
    }

# 2.GET /planets/1 with no data in test database (no fixture) returns a 404
def test_get_one_planet_return_404_with_no_data_in_test_database(client):
    response = client.get("/planets/1")

    assert response.status_code == 404

# 3. GET /planets with valid test data (fixtures) returns a 200 with an array including appropriate test data
def test_get_all_planets(client, all_planets):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Venus", 
            "description": "Venus is the second planet from the Sun.", 
            "size": 12104
        },
        {
            "id": 2,
            "name": "Mars", 
            "description": "Mars is the fourth planet from the Sun and is often called the 'Red Planet'.", 
            "size": 6779
        },
    ]

    # Or use this assert
    assert response_body[0]["id"] == all_planets[0].id
    assert response_body[0]["name"] == all_planets[0].name
    assert response_body[0]["description"] == all_planets[0].description
    assert response_body[0]["size"] == all_planets[0].size

# 4. POST /planets with a JSON request body returns a 201

def test_create_planet(client):
    EXPECTED_PLANET = {
            "name": "Venus", 
            "description": "Venus is the second planet from the Sun.", 
            "size": 12104
    }
    response = client.post("/planets", json=EXPECTED_PLANET)

    response_body = response.get_json()

    assert response.status_code == 201

    assert response_body["id"] == 1
    assert response_body["name"] == EXPECTED_PLANET["name"]
    assert response_body["description"] == EXPECTED_PLANET["description"]
    assert response_body["size"] == EXPECTED_PLANET["size"]

    assert response_body == {
        "id": 1,
        "name": "Venus", 
        "description": "Venus is the second planet from the Sun.", 
        "size": 12104
    }

    # We could further check that the DB was actually updated
    query = db.select(Planet).where(Planet.id == 1)
    new_planet= db.session.scalar(query)  # compare these values to EXPECTED

    assert new_planet.id == 1
    assert new_planet.name == EXPECTED_PLANET["name"]
    assert new_planet.description == EXPECTED_PLANET["description"]
    assert new_planet.size == EXPECTED_PLANET["size"]


# Code Coverage:
#     pytest --cov=app --cov-report html --cov-report term
