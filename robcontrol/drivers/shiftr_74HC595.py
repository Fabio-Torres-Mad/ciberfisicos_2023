# import Adafruit_BBIO.GPIO as GPIO
import logging
import caninos_sdk as k9
import time

LOG = logging.getLogger(__name__)
SER = 7
# _OE = 9
RCLK = 11
SRCLK = 13
_SRCLK = 15

class ShiftRegister:
    register_type = '74HC595'
    

    """
    data_pin => pin 14 on the 74HC595
    latch_pin => pin 12 on the 74HC595
    clock_pin => pin 11 on the 74HC595
    """
    def __init__(self):
        self.labrador = k9.Labrador()
        self.data_pin = SER
        self.latch_pin = RCLK
        self.clock_pin = SRCLK

        self.labrador.pin7.enable_gpio(
            k9.Pin.Direction.OUTPUT,
            alias="data_pin"
        )
        self.labrador.pin7.enable_gpio(
            k9.Pin.Direction.OUTPUT,
            alias="latch_pin"
        )
        self.labrador.pin7.enable_gpio(
            k9.Pin.Direction.OUTPUT,
            alias="clock_pin"
        )

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
        self.labrador.latch_pin.low()

        for i in range(7, -1, -1):
            self.labrador.latch_pin.low()
            self.labrador.clock_pin.high()
            if self.outputs[i] == 0:
                self.labrador.data_pin.low()
            else:
                self.labrador.data_pin.high()
            time.sleep(1)

        self.labrador.latch_pin.high()