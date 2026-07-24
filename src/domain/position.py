import math

class Position:

    def __init__(self, latitude, longitude, altitude):

        if not -90 <= latitude <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees.')

        if not -180 <= longitude <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees.') 
        
        self.latitude = latitude        
        self.longitude = longitude
        self.altitude = altitude


    def __str__(self):
        return (
                f'({self.latitude}, '
                f'{self.longitude}, '
                f'{self.altitude} m)'
                )
    

    def __repr__(self):
        return str(self)


    def __eq__(self, other):

        if not isinstance(other, Position):
            return NotImplemented
        
        return (
                self.latitude == other.latitude
                and self.longitude == other.longitude
                and self.altitude == other.altitude
            )


    def distance_to(self, other):
        
        Earth_radius_meters = 6_371_000                               # Earth radius in meters
        lat1, lat2 = math.radians(self.latitude), math.radians(other.latitude) 
        lon1, lon2 = math.radians(self.longitude), math.radians(other.longitude)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (math.sin(delta_lat/2))**2 + (math.cos(lat1) * math.cos(lat2) * (math.sin(delta_lon/2))**2)

        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1 - a))

        distance = c * Earth_radius_meters

        return  distance                            # calculated in the units of R (meters)
