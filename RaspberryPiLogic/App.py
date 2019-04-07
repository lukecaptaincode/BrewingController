from ServoController import ServoController
from CameraController import CameraController
from TemperatureController import TemperatureController
from FirebaseController import FirebaseController
from SocketController import SocketController
from ExternalReadings import ExternalReadings
import threading
from time import sleep
import RPi.GPIO as GPIO

"""
The main class to run the program, starts multiple threads for each sensor
for reading status, posting data and turning the sensors on and off
"""


class App:
    system_delay = 10  # Entire system delay, data doesnt change often so no need for this to be high
    sensor_data = {'temp': 0, 'camera': ''}
    sensor_status = {'temp': {'ison': {'data': False}, 'threshold': 0}, 'camera': {'ison': {'data': False}},
                     'heater': {'ison': {'data': False}},
                     'servo': {'ison': {'data': False}}, 'external': {'ison': {'data': False}}}
    fb = FirebaseController()
    camera = CameraController('live')
    """
    Gets the status of all sensors from firebase and passes the data into the
    class status object for each object
    """

    def get_sensor_status(self):
        while True:
            sleep(self.system_delay)
            sensorstats = self.fb.get_from_firebase('sensorstat/')
            self.sensor_status['temp'] = sensorstats[0]['temp']
            self.sensor_status['camera'] = sensorstats[0]['camera']
            self.sensor_status['external'] = sensorstats[0]['external']
            self.sensor_status['servo'] = sensorstats[0]['servo']
            self.sensor_status['heater'] = sensorstats[0]['heater']

    """
    Starts and controls sensor operations based on the passed 
    component string, will be threaded
    @param component - the component to control
    """

    def start_sensor(self, component):
        environment = 'live'

        while True:  # Goes forever
            if component == 'servo':
                if self.sensor_status['servo']['ison']['data']:
                    print("Servo is on")
                    servo = ServoController(environment)
                    servo.servo_flip(True)  # If the servo was set to on , open it
                    print("Servo Open")
                    sleep(5)  # Allow some liquid to leave the container
                    servo.servo_flip(False)  # Close the tap
                    print("Servo Close")
                    self.fb.post_to_firebase('sensorstat/' + component + '/ison/data', False)  # turn the servo off
            if component == 'camera':
                if self.sensor_status['camera']['ison']['data']:
                    sleep(self.system_delay)
                    # get the camera to take a picture and retunr the picture as base64
                    self.sensor_data['camera'] = str(self.camera.get_picture())
                    sleep(5)
                    self.fb.post_to_firebase('sensorstat/' + component + '/ison/data', False)  # turn the camera off
            if component == 'temp':
                if self.sensor_status['temp']['ison']['data']:
                    thermo = TemperatureController(environment)
                    sleep(self.system_delay)
                    self.sensor_data['temp'] = thermo.get_temp()
                    """
                    If the average temperature form the thermometers is lower that the threshold
                    turn the heater on by toggling the energenie hat and tell firebase the heater is on
                    if the heater is already on do nothing.
                    
                    Else if the heater is on and the temperature is equal or above the threshold and
                    the heater is on, turn it off
                    """
                    if self.sensor_data['temp'] < self.sensor_status['temp']['threshold']['data']:
                        if self.sensor_status['heater']['ison']['data']:
                            print('too low, heater was already on')
                        else:
                            print('too low, heater is being turned on')
                            self.fb.post_to_firebase('sensorstat/heater/ison/data', True)
                    else:
                        if self.sensor_status['heater']['ison']['data']:
                            print('Temp fine heater off')
                            self.fb.post_to_firebase('sensorstat/heater/ison/data', False)
                        else:
                            print("temp fine")
            if component == 'external':
                if self.sensor_status['external']['ison']:
                    # Get and post the external environment data to firebase
                    extern = ExternalReadings(environment)
                    self.fb.post_to_firebase('external/temp/', extern.get_temp())
                    self.fb.post_to_firebase('external/light/', extern.get_light_level())
                    sleep(self.system_delay)
            if component == 'heater':
                sock = SocketController()
                if self.sensor_status['heater']['ison']['data']:
                    sock.socket_on()
                    sleep(self.system_delay)
                else:
                    sock.socket_off()
                    sleep(self.system_delay)

    """
    Calls the post_to_firbase method and passes sensor data to be sent.
    Each sensor  (except the externals) gets its on thread in which this runs
    Only posts if the sensor is on and if the data isn't 0 - as there is no
    likely event that the sensor data will reach 0
    @params sensor -  the sensor to post
    """

    def post_sensor_data(self, sensor):
        while True:
            if self.sensor_status[sensor]['ison']['data']:
                if sensor == 'servo':
                    sleep(self.system_delay)
                if sensor != 'servo' and self.sensor_data[sensor] != 0:
                    self.fb.post_to_firebase(sensor, self.sensor_data[sensor])
                    sleep(self.system_delay)


"""
Below is the start logic for the entire application it works as follows
The components to run are set as an Array and App instance is created
for each component to run a status thread will be created, which gets if the 
sensor is on or off, after 10 seconds the thread that controlls the component
is started , finally a thread to push data to firebase is started, except if 
the external components are being set (external components control their own data post
as they are not critical)
"""
componentsToRun = ['camera']
app = App
try:
    for comp in componentsToRun:
        print("Up " + comp)
        compStatThread = threading.Thread(target=app.get_sensor_status, args=(app,))
        compStatThread.start()
        print('Sleep for 10 seconds to get sensor status')
        sleep(app.system_delay)
        compThread = threading.Thread(target=app.start_sensor, args=(app, comp))
        compThread.start()
        if comp != 'external':
            compDataPush = threading.Thread(target=app.post_sensor_data, args=(app, comp))
            compDataPush.start()
        else:
            print('External sensors handle their own post, no thread started')
except KeyboardInterrupt:
    print("Bye")
    GPIO.cleanup()
