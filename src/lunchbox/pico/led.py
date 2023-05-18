import time

from machine import PWM, Pin


class Led:
    def __init__(self, channel: int, frequency: int) -> None:
        self.pwm_driver = PWM(Pin(channel))
        self.pwm_driver.freq(frequency)

        self.sleep_s = 0.1

    def drive(self, value: int) -> None:
        self.pwm_driver.duty_u16(value)
        time.sleep(self.sleep_s)
