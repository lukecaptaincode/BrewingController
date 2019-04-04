from ds18b20Reader import DS18B20
from random import randint


class TemperatureController:
    environment = 'test'

    def __init__(self, environment):
        self.environment = environment

    def get_temp(self):
        temp_list = []
        if self.environment != 'test':
            thermometerInterface = DS18B20()
            count = thermometerInterface.device_count()
            i = 0
            while i < count:
                self.temp_list.append(thermometerInterface.tempC(i))
                i += 1
        else:
            i = 0
            while i < 2:
                temp_list.append(randint(5, 20))
                i += 1
        return self.get_average_temp(temp_list)

    def get_average_temp(self, temp_list):
        return sum(temp_list) / len(temp_list)
