from pprint import pprint

import bluesky.plan_stubs as bps
from bluesky.plans import scan
from bluesky.run_engine import RunEngine
from ophyd import EpicsSignal

from lunchbox.bluesky import Consumer
from lunchbox.devices.lunchbox import LunchBox

lunchbox = LunchBox(name="lunchbox")
servo = EpicsSignal("LUNCHBOX:SERVO:RBV", "LUNCHBOX:SERVO", timeout=0.2)

servo.wait_for_connection()


def print_func():
    print("event done!")


consumer = Consumer(print_func)


def scan_diffraction():
    yield from bps.abs_set(lunchbox.directory, ".")
    yield from bps.abs_set(lunchbox.filename, "test")
    yield from scan([lunchbox], servo, 0, 45, 10)
    yield from bps.abs_set(servo, 0.0)


RE = RunEngine()
RE.subscribe(consumer)
RE(scan_diffraction())
