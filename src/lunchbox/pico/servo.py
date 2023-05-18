import time

from machine import PWM, Pin


class Servo:
    def __init__(self, channel: int, frequency: int) -> None:
        self.pwm_driver = PWM(Pin(channel))
        self.pwm_driver.freq(frequency)

        self.duty_at_0_deg = 0.025
        self.duty_at_180_deg = 0.115

        self.sleep_s = 0.1

    def drive(self, value: int) -> None:
        duty_range = self.duty_at_180_deg - self.duty_at_0_deg
        request_duty = int(value * duty_range + self.duty_at_0_deg * 65535)
        self.pwm_driver.duty_u16(request_duty)
        time.sleep(self.sleep_s)
