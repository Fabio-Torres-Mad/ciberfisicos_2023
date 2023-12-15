import time
import logging
import caninos_sdk as k9

from robcontrol.drivers.shiftr_74HC595 import ShiftRegister
from robcontrol.libs.pwm import PWM

LOG = logging.getLogger(__name__)
EN1 = 38    # 0, 1
EN2 = 40
EN10 = 35   # 4, 5
EN20 =  37  # 7, 6

class Motors:

    def __init__(self) -> None:
        LOG.info(f"Init Motors driver")
        self.shiftr = ShiftRegister()
        self.forward_f = False
        
        LOG.info("Configure PWM")
        self.pwm_left = PWM(
            gpio=33, # GPIOB1
            freq=100, duty_cycle=0.1
        )
        self.pwm_right = PWM(
            gpio=34, # GPIOB2
            freq=100, duty_cycle=0.1
        )
        LOG.info("------- init motors: OK -------")

    def forward(self, duty_cycle: float) -> None:
        # self.pwm_left.stop()
        # self.pwm_right.stop()
        self.forward_f = True

        LOG.info(f"Forward...")
        # Clear output
        self.shiftr.outputs = [0] * 8
        self.shiftr.latch()
        
        # Set rotation way for right motor
        self.shiftr.setOutput(4, 0)
        self.shiftr.setOutput(5, 1)
        # Set rotation way for left motor
        self.shiftr.setOutput(7, 0)
        self.shiftr.setOutput(6, 1)
        # Set speed motor
        self.pwm_left.duty_cycle=duty_cycle
        self.pwm_right.duty_cycle=duty_cycle
        self.pwm_left.start()
        self.pwm_right.start()
        self.shiftr.latch()

    def backward(self, duty_cycle: float) -> None:
        self.pwm_left.stop()
        self.pwm_right.stop()
        self.forward_f = False

        LOG.info(f"Backward...")
        # Clear output
        self.shiftr.outputs = [0] * 8
        self.shiftr.latch()

        # Set rotation way for right motor
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 0)
        # Set rotation way for left motor
        self.shiftr.setOutput(7, 1)
        self.shiftr.setOutput(6, 0)
        # Set speed motor
        self.pwm_left.duty_cycle=duty_cycle
        self.pwm_right.duty_cycle=duty_cycle
        self.pwm_left.start()
        self.pwm_right.start()
        self.shiftr.latch()
    
    def to_right(self, duty_cycle: float) -> None:
        self.pwm_left.stop()
        self.pwm_right.stop()
        self.forward_f = False

        LOG.info(f"To right...")
        # Clear output
        self.shiftr.outputs = [0] * 8
        self.shiftr.latch()

        # Stop right motor
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 1)
        # Move left motor
        self.shiftr.setOutput(7, 0)
        self.shiftr.setOutput(6, 1)
        self.pwm_left.duty_cycle=duty_cycle
        self.pwm_left.start()
        self.shiftr.latch()

    def to_left(self, duty_cycle: float) -> None:
        self.pwm_left.stop()
        self.pwm_right.stop()
        self.forward_f = False

        LOG.info(f"To left...")
        # Clear output
        self.shiftr.outputs = [0] * 8
        self.shiftr.latch()

        # Stop left motor
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 1)
        # Move right motor
        self.shiftr.setOutput(7, 0)
        self.shiftr.setOutput(6, 1)
        self.pwm_right.duty_cycle=duty_cycle
        self.pwm_right.start()
        self.shiftr.latch()
    
    def stop(self):
        self.pwm_left.stop()
        self.pwm_right.stop()

        LOG.info(f"Stop motors!")
        # Stop right motor 
        self.shiftr.setOutput(4, 1)
        self.shiftr.setOutput(5, 1)
        # Stop left motor
        self.shiftr.setOutput(7, 1)
        self.shiftr.setOutput(6, 1)
        self.shiftr.latch()
        self.forward_f = False

