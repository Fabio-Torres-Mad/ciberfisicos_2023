import time
import logging
import caninos_sdk as k9

from robcontrol.config import ServoConfig


LOG = logging.getLogger(__name__)


class ServoMotor:
    def __init__(self, conf: ServoConfig) -> None:
        LOG.info(f"Init Servo driver")
        self.conf: conf
        self.labrador = k9.Labrador()
        self.labrador.pin(conf.control).enable_gpio(
            k9.Pin.Direction.OUTPUT
        )

    def right(self) -> None:
        self.labrador.pin(self.conf.control).enable_pwm(
            freq=50,
            duty_cycle=0.025
        )
        self.labrador.pin(self.conf.control).pwm.start()
        sleep(0.5)
        self.labrador.pin(self.conf.control).pwm.stop()

    def center(self) -> None:
        self.labrador.pin(self.conf.control).enable_pwm(
            freq=50,
            duty_cycle=0.075
        )
        self.labrador.pin(self.conf.control).pwm.start()
        sleep(0.5)
        self.labrador.pin(self.conf.control).pwm.stop()

    def left(self) -> None:
        self.labrador.pin(self.conf.control).enable_pwm(
            freq=50,
            duty_cycle=0.12
        )
        self.labrador.pin(self.conf.control).pwm.start()
        sleep(0.5)
        self.labrador.pin(self.conf.control).pwm.stop()