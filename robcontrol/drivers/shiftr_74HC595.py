import logging
# import caninos_sdk as k9
import time
import os

LOG = logging.getLogger(__name__)
SER = 7 # Data 
_OE = 9
RCLK = 11 # Latch/storage
SRCLK = 13  # Shift register
_SRCLK = 15 # GPIOC4

class ShiftRegister:
    register_type = '74HC595'
    """
    data_pin => pin 14 on the 74HC595
    latch_pin => pin 12 on the 74HC595
    shift_pin => pin 11 on the 74HC595
    """
    def __init__(self):
        LOG.info(f"Init ShiftRegister driver")
        # self.labrador = k9.Labrador()
        self.data_pin = 50
        self.latch_pin = 64
        self.shift_pin = 65
        self.reset_pin = 68

        LOG.debug(f"Set data_pin {SER}")
        # pin7: GPIOB18
        os.system(f"sudo sh -c 'echo {self.data_pin} > /sys/class/gpio/export'")
        os.system(f"sudo sh -c 'echo out > /sys/class/gpio/gpio{self.data_pin}/direction'")

        LOG.debug(f"Set latch_pin {RCLK}")
        # pin11: GPIOC0
        os.system(f"sudo sh -c 'echo {self.latch_pin} > /sys/class/gpio/export'")
        os.system(f"sudo sh -c 'echo out > /sys/class/gpio/gpio{self.latch_pin}/direction'")
        
        LOG.debug(f"Set shift_pin {SRCLK}")
        # pin13: GPIOC1
        os.system(f"sudo sh -c 'echo {self.shift_pin} > /sys/class/gpio/export'")
        os.system(f"sudo sh -c 'echo out > /sys/class/gpio/gpio{self.shift_pin}/direction'")

        LOG.debug(f"Set shift_pin {_SRCLK}")
        # pin13: GPIOC1
        os.system(f"sudo sh -c 'echo {self.reset_pin} > /sys/class/gpio/export'")
        os.system(f"sudo sh -c 'echo out > /sys/class/gpio/gpio{self.reset_pin}/direction'")
        os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.reset_pin}/value'")

        self.outputs = [0] * 8

    """
    output_number => Value from 0 to 7 pointing to the output pin on the 74HC595
    0 => Q0 pin 15 on the 74HC595
    1 => Q1 pin 1 on the 74HC595
    2 => Q2 pin 2 on the 74HC595
    3 => Q3 pin 3 on the 74HC595
    4 => Q4 pin 4 on the 74HC595
    5 => Q5 pin 5 on the 74HC595
    6 => Q6 pin 6 on the 74HC595
    7 => Q7 pin 7 on the 74HC595

    value => a state to pass to the pin, could be HIGH or LOW
    """
    def setOutput(self, output_number, value):
        try:
            self.outputs[output_number] = value
        except IndexError:
            raise ValueError("Invalid output number. Can be only an int from 0 to 7")

    def setOutputs(self, outputs):
        if 8 != len(outputs):
            raise ValueError("setOutputs must be an array with 8 elements")

        self.outputs = outputs

    def latch(self):
        # self.labrador.latch_pin.low()
        os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.shift_pin}/value'")
        os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.latch_pin}/value'")
        os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.shift_pin}/value'")

        for i in range(7, -1, -1):
            # os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.latch_pin}/value'")
            os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.shift_pin}/value'")
            os.system(f"sudo sh -c 'echo {self.outputs[i]} > /sys/class/gpio/gpio{self.data_pin}/value'")
            os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.shift_pin}/value'")
            # time.sleep(1)

        # self.labrador.latch_pin.high()
        os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.shift_pin}/value'")
        os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.latch_pin}/value'")
        os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.shift_pin}/value'")