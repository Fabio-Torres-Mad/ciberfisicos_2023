import os
import time
import logging
import threading
import caninos_sdk as k9

from robcontrol.libs.bash import exec
LOG = logging.getLogger(__name__)

class Ultrasound(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.stop_flag = threading.Event()
        self.distance_cm = -1
        self.distance_in = -1
        
        self.trigger_pin = 88
        self.echo_pin = 48

        LOG.info(f"Init Ultrasound driver")
        # pin21: GPIOC24
        os.system(f"sudo sh -c 'echo {self.trigger_pin} > /sys/class/gpio/export'")
        os.system(f"sudo sh -c 'echo out > /sys/class/gpio/gpio{self.trigger_pin}/direction'")

        # pin27: GPIOB16
        os.system(f"sudo sh -c 'echo {self.echo_pin} > /sys/class/gpio/export'")
        os.system(f"sudo sh -c 'echo in > /sys/class/gpio/gpio{self.echo_pin}/direction'")
    
    def measure_distance(self) -> float:
        # Trigger pulse
        os.system(f"sudo sh -c 'echo 1 > /sys/class/gpio/gpio{self.trigger_pin}/value'")
        time.sleep(0.00001) #10us
        os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.trigger_pin}/value'")
        
        time.sleep(0.0002)
        time_s = time.time()
        pulse_start = time.time()
        while (
            exec([
                f"sudo cat /sys/class/gpio/gpio{self.echo_pin}/value"
            ]) == 0
        ):
            pulse_start = time.time()
            if pulse_start - time_s > 0.038:
                LOG.warning("No obstacle!")
                return -1
        
        time_s = time.time()
        pulse_end = time.time()
        while (
            exec([
                f"sudo cat /sys/class/gpio/gpio{self.echo_pin}/value"
            ]) == 1
        ):
            pulse_end = time.time()
            if pulse_end - time_s > 0.038:
                LOG.warning("No obstacle!")
                return -1
        
        # LOG.info(f"{pulse_end} - {pulse_start}")
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 340 / 2
        # LOG.debug(f"New distance: {distance}")
        return distance

    def get_distance(self) -> None:
        LOG.info(f"Getting distance")
        os.system(f"sudo sh -c 'echo 0 > /sys/class/gpio/gpio{self.trigger_pin}/value'")
        time.sleep(5)
        try:
            while True:
                distance = self.measure_distance()
                time.sleep(0.5)
                self.distance_cm = round(distance, 2)
                self.distance_in = round(distance / 2.54, 2)
                # LOG.debug(f"New distance: {self.distance_cm}")
        except KeyboardInterrupt or Exception as e:
            LOG.error(f"Error ocurred during execute get_distance: {e}")
            self.stop()
        else:
            time.sleep(5)

    def stop(self):
        self.stop_flag.set()
