from time import sleep
import base64


class CameraController:
    environment = 'test'
    camera = None

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
    """

    def get_picture(self):
        if self.environment != 'test':
            self.camera.start_preview()
            sleep(5)
            self.camera.capture('tmpImage.jpg')
            self.camera.stop_preview()
        with open("tmpImage.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
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
