class Simulation:

    def __init__(self, world):
        self.world = world

        self.current_time = 1                     # measured in seconds
        self.current_step = 0                     # measured in units of steps
        self.current_state = 'Initialized'        # 'Initialized', 'Running', 'Paused' or 'Stopped'
        

    def start(self):
        if self.current_state == 'Initialized':
            self.current_state = 'Running'


    def resume(self):
        if self.current_state == "Paused":
            self.current_state = "Running"


    def pause(self):
        if self.current_state == 'Running':
            self.current_state = 'Paused'


    def stop(self):
        if self.current_state == 'Running' or self.current_state == 'Paused':
            self.current_state = 'Stopped'

    def step(self):
        if self.current_state == 'Running':
            self.current_step += 1

            self.world.update()
