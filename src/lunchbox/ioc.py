import numpy as np
import serial

# Import the basic framework components.
from softioc import asyncio_dispatcher, builder, softioc

try:
    pico = serial.Serial("/dev/ttyACM0", 115200)
except serial.SerialException:
    pico = serial.Serial("/dev/ttyACM1", 115200)
# Set the record prefix

builder.SetDeviceName("LUNCHBOX")
builder.SetBlocking(True)

led_ai = builder.aIn("LED:RBV", initial_value=0.0)
servo_ai = builder.aIn("SERVO:RBV", initial_value=0.0)

# set min and max angle..
min_angle = 0.0
max_angle = 180.0
angle_range = max_angle - min_angle


def write_to_pico(input: bytes):
    pico.write(input)
    pico.flush()
    return


def update_led(value: float):
    """update the led to a value between 0 and 1.

    1 corresponds to maximal brightness, 0 to minimal.
    """
    angle = servo_ai.get()
    uint16_brightness = int(value * 0xFFFF)
    uint16_angle = int(((angle - min_angle) / angle_range) * 0xFFFF)

    pass_string = b"%d %d\r\n" % (uint16_brightness, uint16_angle)
    write_to_pico(pass_string)

    led_ai.set(value)


def update_servo(value: float):
    led = led_ai.get()
    uint16_brightness = int(np.floor(led * 0xFFFF))
    uint16_angle = int(((value - min_angle) / angle_range) * 0xFFFF)

    pass_string = b"%d %d\r\n" % (uint16_brightness, uint16_angle)
    write_to_pico(pass_string)

    servo_ai.set(value)


led_ao = builder.aOut(
    "LED", initial_value=0.0, on_update=update_led, always_update=True
)
servo_ao = builder.aOut(
    "SERVO", initial_value=0.0, on_update=update_servo, always_update=True
)

# Boilerplate get the IOC started
if __name__ == "__main__":
    builder.LoadDatabase()
    softioc.iocInit(dispatcher=asyncio_dispatcher.AsyncioDispatcher())
    softioc.interactive_ioc(globals())
