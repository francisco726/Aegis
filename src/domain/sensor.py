import math
from domain.fire import Fire
from domain.observation import Observation

class Sensor:

    def __init__(self, field_of_view):
        self.field_of_view = field_of_view                    # Radius that it can scan (eg: 135 deg)


    def calculate_footprint_radius(self, altitude):           # Calculates the radius (meters) of the observed area on the ground

        half_fov = math.radians(self.field_of_view / 2)

        return altitude * math.tan(half_fov)


    def scan(self, observer_position, entities):              # observer_position is an instance (Position) and entities is a list
        print(f'Sensor scanning from {observer_position}')

        detected_observations = []

        for entity in entities:

            if isinstance(entity, Fire):

                if self.is_detectable(entity, observer_position):

                    observation = Observation(
                                              position = entity.position,
                                              measured_intensity = entity.intensity,
                                              confidence = 1.0
                                              )
                    
                    detected_observations.append(observation)

        return detected_observations


    def is_detectable(self, entity, observer_position):
        distance = observer_position.distance_to(entity.position)

        footprint_radius = self.calculate_footprint_radius(observer_position.altitude)

        return distance <= footprint_radius
