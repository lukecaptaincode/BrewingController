from ServoController import ServoController
from CameraController import CameraController
from TemperatureController import TemperatureController
from FirebaseController import FirebaseController
from SocketController import SocketController
import threading
from time import sleep


class App:

    def start_sensor(self, component):
        environment = 'live'
        sleep_time = 5
        while True:
            if component == 'servo':
                servo = ServoController(environment)
                sleep(sleep_time)
                print(servo.servo_flip(True))
            if component == 'camera':
                camera = CameraController(environment)
                sleep(sleep_time)
                print(camera.get_picture())
            if component == 'temp':
                thermo = TemperatureController(environment)
                sleep(sleep_time)
                print(thermo.get_temp())
            if component == 'socket':
                toggle = "true"  # TODO Temp control stuff
                SocketController(toggle)

    #fbController = FirebaseController()


componentsToRun = ['servo']
app = App
for comp in componentsToRun:
    comp = threading.Thread(target=app.start_sensor, args=('component', comp))
    comp.start()
