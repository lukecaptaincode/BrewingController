from gpiozero import Energenie


class SocketController:

    def socket_toggle(self, toggle):
        if toggle:
            Energenie(1).on()
        else:
            Energenie(1).off()
