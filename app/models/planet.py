# Wave 01: Setup and Read

# Flask Setup

# Perform following setup steps for the Solar System API repo to get started on this Flask project:

# Create a virtual environment and activate it
# Install the dependencies
# Define a Planet class with the attributes id, name, and description, and one additional attribute
# Create a list of Planet instances
# RESTful Endpoints: Read

# Create the following endpoint(s), with similar functionality presented in the Hello Books API:

# As a client, I want to send a request...

# ...to get all existing planets, so that I can see a list of planets, with their id, name, description, and other data of the planet.
class Planet:
    def __init__(self, id, name, description, size):
        self.id = id
        self.name = name
        self.description = description
        self.size = size


planets = [
    Planet(1, "Mercury", "The smallest planet in the solar system", 4880),
    Planet(2, "Jupiter", "The larges planet in the solar system", 43400),
    Planet(3, "Venus", "Similar in size to Earth", 12104),
    Planet(4, "Mars", "Smaller terrestrial Planets", 6779)
]