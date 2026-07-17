from world import World
from satellite import Satellite
from fire import Fire
from position import Position
from sensor import Sensor

class Scenario:

    def __init__(self):
        pass


    def create_world(self):
        world = World()
        
        sensor = Sensor(field_of_view = 15.0)

        satellite = Satellite(
            mission_name = 'Sentinel-2A',
            position= Position(
                latitude=41.55,
                longitude=-8.42,
                altitude=700000,
                ),
            sensor = sensor
            )
        
        fire = Fire(position=Position(
                        latitude=41.57,
                        longitude=-8.40,
                        altitude=0,
                    ),
                    intensity = 1.0,
                    radius = 10,
                    spread_rate = 8
                )

        world.add_entity(satellite)
        world.add_entity(fire)

        return world
