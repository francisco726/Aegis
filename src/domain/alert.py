class Alert:

    def __init__(self, detection, state):
        self.detection = detection
        self.state = state


    def __str__(self):
        return (
                f'{self.state} fire at '
                f'{self.detection.observation.position} '
                f'with {self.detection.confidence:.2f} confidence.'
                )
