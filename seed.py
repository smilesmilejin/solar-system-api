# place in a top-level file. call it something like seed.py
# no need to dwell on the `with my_app.app_context():`, other than to say
# that the `db` reference won't work unless it runs with an app context

from app import create_app, db
from app.models.planet import Planet

my_app = create_app()
with my_app.app_context():
    db.session.add(Planet(name="Venus", description="Venus is the second planet from the Sun.", size=12104)),
    db.session.add(Planet(name="Mars", description="Mars is the fourth planet from the Sun and is often called the 'Red Planet'.", size=6779)),
    db.session.add(Planet(name="Jupiter", description="Largest planet in the solar system", size=14300)),
    db.session.add(Planet(name="Saturn", description="Gas giant with rings", size=116500)),

    db.session.commit()