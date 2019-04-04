from time import sleep


class ServoController:
    environment = "test"
    classGPIO = None
    pwm = None

    def __init__(self, environment):
        self.environment = environment
        if self.environment != 'test':
            import RPi.GPIO as GPIO
            self.classGPIO = GPIO
            self.classGPIO.setmode(GPIO.BOARD)
            self.classGPIO.setup(3, GPIO.OUT)
            self.pwm = self.classGPIO.PWM(3, 50)
            self.pwm.start(0)

    def servo_flip(self, is_open):
        if self.environment != 'test':
            if is_open:
                duty = 90 / 18 + 2
            else:
                duty = 180 / 18 + 2
            self.classGPIO.output(3, True)
            self.pwm.ChangeDutyCycle(duty)
            sleep(1)
            self.pwm.output(3, False)
            self.pwm.ChangeDutyCycle(0)
        return is_open
