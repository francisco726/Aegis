from domain.alert import Alert

class AlertEngine:

    def __init__(self):
        self.alert_history = []


    def create_alert(self, detections):

        alerts = []

        for detection in detections:

            if 0.5 <= detection.confidence < 0.75:
                state = "Important"

            elif 0.75 <= detection.confidence <= 1.0:
                state = "Severe"

            else:
                state = "Ignored"

            alert = Alert(detection, state)

            self.alert_history.append(alert)
            alerts.append(alert)

        return alerts
