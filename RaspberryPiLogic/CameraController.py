from time import sleep
import base64
import requests
"""
Controls the taking of pictures and returning of image data
"""
class CameraController:
    environment = 'test'
    camera = None
    """
    init, sets environment and imports the camera lib if live
    """
    def __init__(self, environment):
        self.environment = environment
        if self.environment != 'test':
            try:
                from picamera import PiCamera
            except:
                print("error importing picamera")
            self.camera = PiCamera()

    """
    Gets the image from the camera, saves it to a file, converts the file
    to base64 and returns the base64
    @return encoded_string - the image in base64
    """
    def get_picture(self):
        if self.environment != 'test':
            self.camera.resolution = (500, 500)
            self.camera.start_preview()  # open camera
            sleep(2)
            self.camera.capture('tmpImage.jpg')  # Create temp image
            sleep(5)
        #  Open the image and convert it to base64, then return the value
            with open("tmpImage.jpg", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            self.camera.stop_preview()  # turn cam off
            return encoded_string

    """
    Test Method , used to check base64 image encoding is correct
    @param base64_img: String - the string to build to an image
    """
    def build_image(self, base64_img):
        image = base64.b64decode(base64_img)
        name = 'testImage.jpg'
        with open(name, 'wb') as f:
            f.write(image)
