from enum import Enum

class Simulationstate(Enum):

    INITIALIZED = 'Initialized'
    RUNNING = 'Running'
    PAUSED = 'Paused'
    STOPPED = 'Stopped'
