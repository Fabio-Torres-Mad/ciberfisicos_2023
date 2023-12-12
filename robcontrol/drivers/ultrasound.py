import os
import time
import logging
import threading
import caninos_sdk as k9

LOG = logging.getLogger(__name__)

class Ultrasound(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.stop_flag = threading.Event()
        self.distance_cm = -1
        self.distance_in = -1

        LOG.info(f"Init Ultrasound driver")
        self.labrador = k9.Labrador()
        self.labrador.pin21.enable_gpio(
            k9.Pin.Direction.OUTPUT,
            alias="trigger_pin"
        )
        self.labrador.pin27.enable_gpio(
            k9.Pin.Direction.INPUT,
            alias="echo_pin"
        )
    
    def measure_distance(self) -> float:
        # Trigger pulse
        self.labrador.trigger_pin.high()
        time.sleep(0.00001) #10us
        self.labrador.trigger_pin.low()
        
        time.sleep(0.0002)
        time_s = time.time()
        pulse_start = time.time()
        while (
            self.labrador.echo_pin.read() == 0
        ):
            pulse_start = time.time()
            if pulse_start - time_s > 0.038:
                LOG.warning("No obstacle!")
                return -1
        
        time_s = time.time()
        pulse_end = time.time()
        while (
            self.labrador.echo_pin.read() == 1
        ):
            pulse_end = time.time()
            if pulse_end - time_s > 0.038:
                LOG.warning("No obstacle!")
                return -1
        
        LOG.info(f"{pulse_end} - {pulse_start}")
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2
        LOG.info(f"New distance: {distance}")
        return distance

    def get_distance(self) -> None:
        LOG.info(f"Getting distance")
        self.labrador.trigger_pin.low()
        time.sleep(5)
        try:
            while True:
                distance = self.measure_distance()
                self.distance_cm = round(distance, 2)
                self.distance_in = round(distance / 2.54, 2)
        except KeyboardInterrupt or Exception as e:
            LOG.error(f"Error ocurred during execute get_distance: {e}")
            self.stop()
        else:
            time.sleep(5)

    def stop(self):
        self.stop_flag.set()
