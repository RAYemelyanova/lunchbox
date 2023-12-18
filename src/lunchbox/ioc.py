"""Creates a pythonSoftIoc to wrap the laser and servo."""
from lunchbox.pwm import Laser, Servo

from softioc import asyncio_dispatcher, builder, softioc

from functools import partial

builder.SetDeviceName("LUNCHBOX")
builder.SetBlocking(True)

laser_ai = builder.aIn("LASER:RBV", initial_value = 0.0)
servo_ai = builder.aIn("SERVO:RBV", initial_value = 0.0)

def update_servo(servo: Servo, value: float):
    """Set the servo value."""
    servo.set(value)
    servo_ai.set(value)

def update_laser(laser: Laser, value: float):
    """Set the laser value."""
    laser.set(value)
    laser_ai.set(value)


if __name__ == "__main__":
    servo = Servo(500, 2300, 0.0, 180.0)
    laser = Laser(50000)

    laser_ao = builder.aOut(
        "LASER",
        initial_value=0.0,
        on_update=partial(update_laser, laser),
        always_update=True
    )
    servo_ao = builder.aOut(
        "SERVO",
        initial_value=0.0,
        on_update=partial(update_servo, servo),
        always_update=True
    )
    builder.LoadDatabase()
    softioc.iocInit(dispatcher=asyncio_dispatcher.AsyncioDispatcher())
    softioc.interactive_ioc(globals())
