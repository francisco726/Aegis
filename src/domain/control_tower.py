from domain.detection_engine import DetectionEngine
from domain.alert_engine import AlertEngine

class ControlTower:

    def __init__(self):
        self.detection_engine = DetectionEngine()
        self.alert_engine = AlertEngine()


    def process(self, observations):

        detections = self.detection_engine.detect(observations)

        alerts = self.alert_engine.create_alert(detections)

        return alerts
