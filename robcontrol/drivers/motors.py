import time
import logging
import caninos_sdk as k9

from robcontrol.config import MotorConfig, MotorChannel


LOG = logging.getLogger(__name__)

class Motors:
    def __init__(self, conf: MotorConfig) -> None:
        LOG.info(f"Init Motors driver")
        self.labrador = k9.Labrador()

        # Right motor config
        self.right_motor = conf.m_right
        self._set_pins(self.right_motor)
        self._set_pwm(self.right_motor.ENA, 0)
        
        # Left motor config
        self.left_motor = conf.m_left
        self._set_pins(self.left_motor)
        self._set_pwm(self.left_motor.ENA, 0)
    
    def _set_pins(self, chn: MotorChannel) -> None:
        try:
            self.labrador.pin(chn.IN0).enable_gpio(
                k9.Pin.Direction.OUTPUT
            )
            self.labrador.pin(chn.IN1).enable_gpio(
                k9.Pin.Direction.OUTPUT
            )
        except Exception as e:
            LOG.error(f"Some error occurred: {e}")

    def _set_pwm(
        self,
        chn: MotorChannel,
        duty_cycle: float
    ) -> None:
        LOG.info(f"Configure PWM to {duty_cycle * 100}%")
        self.labrador.pin(chn.ENA).enable_pwm(
            freq=100,
            duty_cycle=duty_cycle
        )

    def forward(self, duty_cycle: float) -> None:
        LOG.info(f"Forward...")
        # Set rotation way for right motor
        self.labrador.pin(self.conf.right_motor.IN0).low()
        self.labrador.pin(self.conf.right_motor.IN1).high()
        # Set rotation way for left motor
        self.labrador.pin(self.conf.left_motor.IN0).low()
        self.labrador.pin(self.conf.left_motor.IN1).high()
        # Set speed motor
        self._set_pwm(self.right_motor, duty_cycle)
        self._set_pwm(self.left_motor, duty_cycle)
        self.labrador.pin(self.right_motor.ENA).pwm.start()
        self.labrador.pin(self.left_motor.ENA).pwm.start()

    def backward(self, duty_cycle: float) -> None:
        LOG.info(f"Backward...")
        # Set rotation way for right motor
        self.labrador.pin(self.conf.right_motor.IN0).high()
        self.labrador.pin(self.conf.right_motor.IN1).low()
        # Set rotation way for left motor
        self.labrador.pin(self.conf.left_motor.IN0).high()
        self.labrador.pin(self.conf.left_motor.IN1).low()
        # Set speed motor
        self._set_pwm(self.right_motor, duty_cycle)
        self._set_pwm(self.left_motor, duty_cycle)
        self.labrador.pin(self.right_motor.ENA).pwm.start()
        self.labrador.pin(self.left_motor.ENA).pwm.start()
    
    def to_right(self, duty_cycle: float) -> None:
        # Stop right motor
        self.labrador.pin(self.conf.right_motor.IN0).high()
        self.labrador.pin(self.conf.right_motor.IN1).high()
        # Move left motor
        self.labrador.pin(self.conf.left_motor.IN0).low()
        self.labrador.pin(self.conf.left_motor.IN1).high()
        self._set_pwm(self.left_motor, duty_cycle)
        self.labrador.pin(self.left_motor.ENA).pwm.start()

    def to_left(self, duty_cycle: float) -> None:
        # Stop left motor
        self.labrador.pin(self.conf.left_motor.IN0).high()
        self.labrador.pin(self.conf.left_motor.IN1).high()
        # Move right motor
        self.labrador.pin(self.conf.right_motor.IN0).low()
        self.labrador.pin(self.conf.right_motor.IN1).high()
        self._set_pwm(self.right_motor, duty_cycle)
        self.labrador.pin(self.right_motor.ENA).pwm.start()
    
    def stop(self):
        LOG.info(f"Stop motors!")
        # Stop right motor 
        self.labrador.pin(self.conf.right_motor.IN0).high()
        self.labrador.pin(self.conf.right_motor.IN1).high()
        # Stop left motor
        self.labrador.pin(self.conf.left_motor.IN0).high()
        self.labrador.pin(self.conf.left_motor.IN1).high()

