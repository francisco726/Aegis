class Detection:

    def __init__(
                 self,
                 observation,
                 is_fire,
                 confidence
                 ):
        
        self.observation = observation
        self.is_fire = is_fire
        self.confidence = confidence


    def __str__(self):

        return (
            f"Detection("
            f"is_fire={self.is_fire}, "
            f"confidence={self.confidence:.2f}, "
            f"{self.observation}"
            f")"
        )


    def __repr__(self):
        return str(self)
