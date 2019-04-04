from time import sleep
import RPi.GPIO as GPIO

class ServoController:
    environment = "test"
    classGPIO = None
    pwm = None

    def __init__(self, environment):
        self.environment = environment


    def servo_flip(self, is_open):
        self.classGPIO = GPIO
        self.classGPIO.setmode(GPIO.BOARD)
        self.classGPIO.setup(03, GPIO.OUT)
        self.pwm = self.classGPIO.PWM(03, 50)
        self.pwm.start(0)
        if self.environment != 'test':
            if is_open:
                duty = 90 / 18 + 2
            else:
                duty = 180 / 18 + 2
            self.classGPIO.output(03, True)
            self.pwm.ChangeDutyCycle(duty)
            sleep(1)
            self.pwm.output(03, False)
            self.pwm.ChangeDutyCycle(0)
        return is_open
