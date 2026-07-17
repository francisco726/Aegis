from entity import Entity
from satellite import Satellite
from control_tower import ControlTower

class World:

    def __init__(self):
        self.entities = []                      # guarda todas as entidades que representam o estado atual da simulação
        self.control_tower = ControlTower()


    def add_entity(self,entity):
        if isinstance(entity,Entity) and entity not in self.entities:         # prevents repeated entities and only accepts entites from the Entity class
            self.entities.append(entity) 


    def remove_entity(self, entity):            # .remove(name) and .pop(index)
        if isinstance(entity, Entity) and entity in self.entities:
            self.entities.remove(entity)


    def print_state(self):
        print(f'Number of entities: {len(self.entities)}')
        print(f'Entities: {', '.join(str(entity) for entity in self.entities)}')


    def update(self):                           # context is a dictionary containing simulation data, 'entities' stores the list of entity objects currently in the World

        context = {'entities': self.entities}

        for entity in self.entities:
            entity.update(context)

        observations = []                       # collects all observations produced by the entities during this simulation step

        for entity in self.entities:
            observations.extend(entity.get_observations())

        detections = self.control_tower.process_observations(observations)  # processes observations

        # Temporary debugging output
        for detection in detections:
            print(detection)
