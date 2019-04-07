from ds18b20Reader import DS18B20
from random import randint

"""
This class reads data from the thermoeters and returns the average
makes use of the ds18b20Reader class to do this
"""
class TemperatureController:
    environment = 'test'

    """
    Inits the class and environ
    """
    def __init__(self, environment):
        self.environment = environment

    """
    Gets the temp from the thermometers if we're live,
    for each thermoeter found the value of celsius is added to a temp_list
    else random ints are generated to the size of two thermometers
    @return average_temp - float
    """
    def get_temp(self):
        temp_list = []
        if self.environment != 'test':
            thermometerInterface = DS18B20()  # init class
            count = thermometerInterface.device_count()  # get connect devices
            i = 0
            while i < count:
                temp_list.append(thermometerInterface.tempC(i))  # loop into list
                i += 1
        else:
            i = 0
            while i < 2:
                temp_list.append(randint(5, 23))  # dummy data
                i += 1
        # pass the list to the get_average_temp method so the all the data in the list will be average
        return self.get_average_temp(temp_list)
    """
    For the gets the average of the passed list of temps
    @param  temp_list -  list of temps
    """
    def get_average_temp(self, temp_list):
        return sum(temp_list) / len(temp_list)  # the sum of all values in the list divided by the length
