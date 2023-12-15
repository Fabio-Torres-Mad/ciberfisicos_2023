import threading, timeit, logging
import os
from robcontrol.libs.bash import exec

class PWM:
    freq = 0
    duty_cycle = 0
    period_high = 0
    period_low = 0
    thread: any
    gpio: any
    running: bool

    def __init__(
        self,
        gpio:int,
        freq: int,
        duty_cycle: float,
    ) -> None:
        self.gpio = gpio
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.period_high = duty_cycle / freq
        self.period_low = (1 - duty_cycle) / freq
        logging.debug(f"Set pin {gpio}")
        if not exec([
            f"ls /sys/class/gpio/gpio{gpio}"
        ]):
            os.system(f"sudo sh -c 'echo {gpio} > /sys/class/gpio/export'")
            os.system(f"sudo sh -c 'echo out > /sys/class/gpio/gpio{gpio}/direction'")

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.running = 1
        self.thread.start()

    def stop(self):
        self.running = 0

    def run(self):
        state = True
        os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.gpio}/value'")
        start = timeit.default_timer()
        while self.running:
            passed_time = timeit.default_timer() - start
            if state:
                if passed_time >= self.period_high:
                    os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.gpio}/value'")
                    state = False
                    start = timeit.default_timer()
            else:
                if passed_time >= self.period_low:
                    os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.gpio}/value'")
                    state = True
                    start = timeit.default_timer()
        os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.gpio}/value'")