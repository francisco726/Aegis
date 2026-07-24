from domain.satellite import Satellite
from domain.fire import Fire

class SimulationSnapshot:

    def __init__(
                 self,
                 step,
                 simulation_state,
                 entities,
                 alerts
                 ):
        
        self.step = step
        self.simulation_state = simulation_state
        self.entities = entities
        self.alerts = alerts


    def __str__(self):
        return (
                f'step = {self.step} \n' 
                f'state: {self.simulation_state} \n'
                f'entities: {', '.join(str(entity) for entity in self.entities)} \n' 
                f'alerts: {' ,'.join(str(entity) for entity in self.entities)} \n'
                )


    @property
    def satellite(self):
        return [entity for entity in self.entities if isinstance(entity, Satellite)]
    

    @property
    def fire(self):
        return [entity for entity in self.entities if isinstance(entity, Fire)]
