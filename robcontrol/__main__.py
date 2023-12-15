import time
import logging
import threading

from robcontrol.libs.logger import setup_logger
from robcontrol.libs.parser import get_parser
from robcontrol.drivers.motors import Motors
from robcontrol.drivers.servo import ServoMotor
from robcontrol.drivers.ultrasound import Ultrasound

LOG = logging.getLogger(__name__)

def take_decision(driver_motor, ultrasound_driver, servo_driver):
    # driver_motor.stop()
    time.sleep(0.5)
    servo_driver.right()
    time.sleep(1)
    dist_right = ultrasound_driver.distance_cm
    while dist_right < 0:
        dist_right = ultrasound_driver.distance_cm
    LOG.info(f"right distance {dist_right}")
    servo_driver.left()
    time.sleep(1)
    dist_left = ultrasound_driver.distance_cm
    while dist_left < 0:
        dist_left = ultrasound_driver.distance_cm
    LOG.info(f"left distance {dist_left}")
    servo_driver.center()
    time.sleep(0.5)

    if dist_right > dist_left:
        LOG.debug("Move to right")
        driver_motor.backward(0.5)
        time.sleep(1)
        driver_motor.to_right(0.5)
        time.sleep(2)
        driver_motor.forward(0.5)
    else:
        LOG.debug("Move to left")
        driver_motor.backward(0.5)
        time.sleep(1)
        driver_motor.to_left(0.5)
        time.sleep(2)
        driver_motor.forward(0.5)


def main():
    """Main function."""
    # Init constructors
    motors = Motors()
    servo = ServoMotor()
    ultrasound = Ultrasound()

    thread = threading.Thread(
        target=ultrasound.get_distance
    )
    thread.start()
    
    # Center servo
    servo.center()

    while True:
        if not motors.forward_f:
            motors.forward(0.5)
        
        try:
            time.sleep(0.1)
            if ultrasound.distance_cm < 10 and ultrasound.distance_cm > 0:
                motors.stop()
                LOG.info(f"Distance: {ultrasound.distance_cm}")
                take_decision(motors, ultrasound, servo)
                time.sleep(5)
            
        except Exception as e:
            LOG.error(f"Stopping program: {e}")
            break
    
    servo.left()
    thread.raise_exception()
    thread.join()

if __name__ == "__main__":
    parser = get_parser(description="Robot Control")
    args = parser.parse_args()
    setup_logger(args.log_level, args.stream_output)
    main()