import time
import logging
import os
import caninos_sdk as k9
# from robcontrol.libs.pwm import PW

LOG = logging.getLogger(__name__)

class ServoMotor:
    def __init__(self) -> None:
        LOG.info(f"Init Servo driver")
        self.labrador = k9.Labrador()

    def left(self) -> None:
        LOG.info("Servo to left")
        self.labrador.pin33.enable_pwm(alias="servo", freq=50, duty_cycle=0.12)
        LOG.debug("Start left")
        self.labrador.servo.pwm.start()
        time.sleep(0.5)
        LOG.debug("Stop left")
        self.labrador.servo.pwm.stop()


    def center(self) -> None:
        LOG.info("Servo to center")
        self.labrador.pin33.enable_pwm(alias="servo", freq=50, duty_cycle=0.07)
        LOG.debug("Start center")
        self.labrador.servo.pwm.start()
        time.sleep(0.4)
        LOG.debug("Stop center")
        self.labrador.servo.pwm.stop()

    def right(self) -> None:
        LOG.info("Servo to right")
        self.labrador.pin33.enable_pwm(alias="servo", freq=50, duty_cycle=0.02)
        LOG.debug("Start left")
        self.labrador.servo.pwm.start()
        time.sleep(0.5)
        LOG.debug("Stop left")
        self.labrador.servo.pwm.stop()
