from domain.detection import Detection

class DetectionEngine:

    def __init__(self):
        pass


    def detect(self, observations):
        
        detection_list = []

        for observation in observations:
            detection = Detection(observation = observation,
                                  is_fire = True,
                                  confidence = observation.confidence
                                  )
            detection_list.append(detection)

        return detection_list
