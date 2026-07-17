from entity import Entity

class Fire(Entity):

    def __init__(
                 self, 
                 position, 
                 intensity, 
                 radius, 
                 spread_rate
                 ):
        
        super().__init__(position)
        
        self.intensity = intensity           # from 0 to 1, 0 being the lowest
        self.radius = radius                 # radius of fire, measured in meters
        self.spread_rate = spread_rate       # m/s, needs to be influenced by the weather and vegetation in future versions


    def __str__(self):
        return (
                f'Fire #{self.id} '
                f'at {self.position} '
                f'(intensity = {self.intensity}) '
                f'(radius = {self.radius} m)'
                )

    
    def __repr__(self):
        return str(self)


    def update(self, context):
        self.radius += self.spread_rate
