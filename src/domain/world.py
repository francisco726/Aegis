from domain.entity import Entity
from domain.control_tower import ControlTower

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


    def update(self):

        context = {'entities': self.entities}

        for entity in self.entities:
            entity.update(context)

        observations = []

        for entity in self.entities:
            observations.extend(entity.get_observations())

        alerts = self.control_tower.process(observations)

        return alerts
