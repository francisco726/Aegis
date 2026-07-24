from domain.simulation_snapshot import SimulationSnapshot
from domain.simulation_state import Simulationstate

class Simulation:

    def __init__(self, world):
        self.world = world

        self.current_time = 1                                          # measured in seconds
        self.current_step = 0                                          # measured in units of steps
        self.current_state = Simulationstate.INITIALIZED               # 'Initialized', 'Running', 'Paused' or 'Stopped'
        

    def start(self):
        if self.current_state in (Simulationstate.INITIALIZED, Simulationstate.STOPPED):
            self.current_state = Simulationstate.RUNNING


    def resume(self):
        if self.current_state == Simulationstate.PAUSED:
            self.current_state = Simulationstate.RUNNING


    def pause(self):
        if self.current_state == Simulationstate.RUNNING:
            self.current_state = Simulationstate.PAUSED


    def stop(self):
        if self.current_state in (Simulationstate.RUNNING, Simulationstate.PAUSED):
            self.current_state = Simulationstate.STOPPED


    def step(self):
        if self.current_state != Simulationstate.RUNNING:
            return None

        self.current_step += 1

        alerts = self.world.update()

        return SimulationSnapshot(
            self.current_step,
            self.current_state,
            self.world.entities,
            alerts
        )