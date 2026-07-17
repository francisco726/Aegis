from detection_engine import DetectionEngine

class ControlTower:

    def __init__(self):
        self.detection_engine = DetectionEngine()


    def process_observations(self, observations):
        return self.detection_engine.detect(observations = observations)

        