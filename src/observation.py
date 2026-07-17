class Observation:

    def __init__(
                 self,
                 position,
                 measured_intensity,
                 confidence
                 ):
        
        self.position = position
        self.measured_intensity = measured_intensity
        self.confidence = confidence


    def __str__(self):
        return (
                f'Observation at {self.position} '
                f'(intensity={self.measured_intensity}, '
                f'confidence={self.confidence})'
                )


    def __repr__(self):
        return str(self)
