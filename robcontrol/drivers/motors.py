import time
import logging
import caninos_sdk as k9

from robcontrol.drivers.shiftr_74HC595 import ShiftRegister

LOG = logging.getLogger(__name__)

class Motors:
    EN1 = 38    # 0, 1
    EN2 = 40
    EN10 = 35   # 4, 5
    EN20 =  37  # 7, 6

    def __init__(self) -> None:
        LOG.info(f"Init Motors driver")
        self.shiftr = ShiftRegister()
        self.labrador = k9.Labrador()

        # Configure PWM motor control
        self.labrador.pin37.enable_pwm(
            freq=100,
            duty_cycle=100,
            alias="pwm_left"
        )
        self.labrador.pin35.enable_pwm(
            freq=100,
            duty_cycle=100,
            alias="pwm_right"
        )

    def forward(self, duty_cycle: float) -> None:
        LOG.info(f"Forward...")
        # Set rotation way for right motor
        self.shiftr.setOutput(4, 0)
        self.shiftr.setOutput(5, 1)
        # Set rotation way for left motor
        self.shiftr.setOutput(7, 0)
        self.shiftr.setOutput(6, 1)
        # Set speed motor
        self.labrador.pwm_left.enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )
        self.labrador.pwm_right.enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )
        self.labrador.pwm_left.pwm.start()
        self.labrador.pwm_right.pwm.start()
        self.shiftr.latch()

    def backward(self, duty_cycle: float) -> None:
        LOG.info(f"Backward...")
        # Set rotation way for right motor
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 0)
        # Set rotation way for left motor
        self.shiftr.setOutput(7, 1)
        self.shiftr.setOutput(6, 0)
        # Set speed motor
        self.labrador.pwm_left.enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )
        self.labrador.pwm_right.enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )
        self.labrador.pwm_left.pwm.start()
        self.labrador.pwm_right.pwm.start()
        self.shiftr.latch()
    
    def to_right(self, duty_cycle: float) -> None:
        # Stop right motor
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 1)
        # Move left motor
        self.shiftr.setOutput(7, 0)
        self.shiftr.setOutput(6, 1)
        self.labrador.pwm_left.enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )
        self.labrador.pwm_right.pwm.start()
        self.shiftr.latch()

    def to_left(self, duty_cycle: float) -> None:
        # Stop left motor
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 1)
        # Move right motor
        self.shiftr.setOutput(7, 0)
        self.shiftr.setOutput(6, 1)
        self.labrador.pwm_right.enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )
        self.labrador.pwm_right.pwm.start()
        self.shiftr.latch()
    
    def stop(self):
        LOG.info(f"Stop motors!")
        # Stop right motor 
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 1)
        # Stop left motor
        self.shiftr.setOutput(7, 1)
        self.shiftr.setOutput(6, 1)
        self.shiftr.latch()

