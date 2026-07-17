from satellite import Satellite

class Entity:

    next_id = 0                         # Shared counter used to generate unique identifiers.

    def __init__(self, position):
        self.id = Entity.next_id
        Entity.next_id += 1

        self.position = position


    def update(self, context):
        pass


    def get_observations(self):
        return []
