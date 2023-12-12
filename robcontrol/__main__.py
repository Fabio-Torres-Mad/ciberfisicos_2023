import time
import logging
import threading

from robcontrol.libs.logger import setup_logger
from robcontrol.libs.parser import get_parser
from robcontrol.drivers.motors import Motors
# from robcontrol.drivers.servo import ServoMotor
from robcontrol.drivers.ultrasound import Ultrasound

LOG = logging.getLogger(__name__)

def take_decision(driver_motor, ultrasound_driver, servo_driver):
    driver_motor.stop()
    time.sleep(0.5)
    servo_driver.right()
    time.sleep(1)
    dist_right = ultrasound_driver.distance_cm
    while dist_right < 0:
        dist_right = ultrasound_driver.distance_cm
    servo_driver.left()
    time.sleep(1)
    dist_left = ultrasound_driver.distance_cm
    while dist_left < 0:
        dist_left = ultrasound_driver.distance_cm
    servo_driver.center()
    time.sleep(0.5)

    if dist_right > dist_left:
        LOG.debug("Move to right")
        driver_motor.backward(0.25)
        time.sleep(0.6)
        driver_motor.to_right(0.25)
        time.sleep(2)
        driver_motor.forward(0.25)
    else:
        LOG.debug("Move to left")
        driver_motor.backward(0.25)
        time.sleep(0.6)
        driver_motor.to_left(0.25)
        time.sleep(2)
        driver_motor.forward(0.25)


def main():
    """Main function."""
    # Init constructors
    motors = Motors()
    # servo = ServoMotor(DEFAULT_CONF['servo'])
    ultrasound = Ultrasound()

    thead = threading.Thread(
        target=ultrasound.get_distance
    )
    thead.start()

    while True:
        try:
            motors.forward(0.5)
            time.sleep(0.080)
            if ultrasound.distance_cm < 20 and ultrasound.distance_cm > 0:
                LOG.info(f"Distance: {ultrasound.distance_cm}")
                # take_decision(motors, ultrasound, servo)
                time.sleep(100)
        except Exception as e:
            LOG.error(f"Stopping program: {e}")
            break
    
    thead.stop()
    thead.join()

if __name__ == "__main__":
    parser = get_parser(description="Robot Control")
    args = parser.parse_args()
    setup_logger(args.log_level, args.stream_output)
    main()