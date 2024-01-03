"""Demonstrates how to control the laser and servo with PWM"""
import pigpio

SERVO_CHANNEL = 18
LED_CHANNEL = 19

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Cannot connect pi to pigpio")


class Servo:
    """Control the servo angle, using pulse width values that match known angles.

    Angle can be in either radians or degrees as long as it is consistent.
    """

    def __init__(
        self, min_pw: int, max_pw: int, min_angle: float, max_angle: float
    ) -> None:
        self.minimum_pulsewidth = min_pw
        self.maximum_pulsewidth = max_pw
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.pi = pigpio.pi()

    def set(self, angle: float) -> None:
        """Set the servo angle."""
        if angle < self.min_angle or angle > self.max_angle:
            raise RuntimeError(f"{angle} degrees beyond the servo angle bounds.")

        angle_ratio = (self.min_angle + angle) / (self.min_angle + self.max_angle)
        pulsewidth = (
            self.maximum_pulsewidth - self.minimum_pulsewidth
        ) * angle_ratio + self.minimum_pulsewidth

        self.pi.set_servo_pulsewidth(SERVO_CHANNEL, pulsewidth)


class Laser:
    """Control the laser brightness using a given frequency."""

    def __init__(self, frequency: int) -> None:
        self.pi = pigpio.pi()
        self.frequency = frequency

    @property
    def frequency(self):
        """Get the frequency of the laser."""
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: int):
        """Set the frequency of the laser."""
        self._frequency = frequency
        self.pi.set_PWM_frequency(LED_CHANNEL, frequency)

    def set(self, duty_cycle: int) -> None:
        """Set laser intensity, with duty_cycle between 0 and 100."""
        self.pi.set_PWM_dutycycle(LED_CHANNEL, duty_cycle)
