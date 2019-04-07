from random import randint

"""
Gets the external readings of the brewing container using a grovepi
"""
class ExternalReadings:
    # sensor ports
    light_sensor = 0
    temp_sensor = 2
    GROVE = None
    environ = 'test'
    """
    Init the class if we're not testing import grovepi and setup the sensor
    inputs
    """
    def __init__(self, environment):
        self.environ = environment
        if self.environ != 'test':
            import grovepi
            self.GROVE = grovepi
            grovepi.pinMode(self.light_sensor, "INPUT")
            grovepi.pinMode(self.temp_sensor, "INPUT")
    """
    Returns the light level from the sensor or a random int
    """
    def get_light_level(self):
        if self.environ != 'test':
            return self.GROVE.analogRead(self.light_sensor)
        else:
            return randint(0, 10)
    """
    Returns the temperature  from the sensor or a random int
    """
    def get_temp(self):
        if self.environ != 'test':
            return self.GROVE.analogRead(self.temp_sensor)
        else:
            return randint(0, 20)
