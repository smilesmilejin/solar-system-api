# Wave 6
import pytest
from app import create_app 
from app.db import db
from flask.signals import request_finished 
from dotenv import load_dotenv 
import os
from app.models.planet import Planet


# python-detenv
load_dotenv() 

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI') # Connect to Test Database
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app 

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_planet(app):
    planet = Planet(
        id=1,
        name="Earth",
        description="Earth is the third planet from the Sun ",
        size=12742
    )

    db.session.add(planet)
    db.session.commit()

    return planet

@pytest.fixture
def all_planets(app):
    # Arrange
    venus_planet = Planet(
        id=1,
        name="Venus", 
        description="Venus is the second planet from the Sun.", 
        size=12104
    )

    mars_planet = Planet(
        id=2,
        name="Mars", 
        description="Mars is the fourth planet from the Sun and is often called the 'Red Planet'.", 
        size=6779)

    db.session.add_all([venus_planet, mars_planet])
    db.session.commit()

    planets_list = [venus_planet, mars_planet]
    return planets_list

