import RPi.GPIO as GPIO
import time

"""
Controls the tap servo
"""


class ServoController:
    environment = "test"
    classGPIO = None
    pwm = None
    """
    Init, if we're not in testing set the gpio
    """

    def __init__(self, environment):
        self.environment = environment

    """
    Flips the servo open and closed
    @param is_open - bool
    @return is_open - bool
    """

    def servo_flip(self, is_open):
        if self.environment != 'test':
            servoPIN = 17
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(servoPIN, GPIO.OUT)
            p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
            p.start(2.5)  # Initialization
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(12.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            time.sleep(0.5)
            p.stop()
        return is_open
