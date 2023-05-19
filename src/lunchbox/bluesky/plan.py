from pprint import pprint

import bluesky.plan_stubs as bps
import matplotlib.pyplot as plt
from bluesky.plans import scan
from bluesky.run_engine import RunEngine
from ophyd import EpicsSignal

from lunchbox.bluesky import Consumer
from lunchbox.devices.lunchbox import LunchBox

lunchbox = LunchBox(name="lunchbox")
servo = EpicsSignal("LUNCHBOX:SERVO:RBV", "LUNCHBOX:SERVO", timeout=0.2)

servo.wait_for_connection()


def scan_diffraction():
    yield from bps.abs_set(lunchbox.directory, ".")
    yield from bps.abs_set(lunchbox.filename, "test")
    yield from bps.abs_set(lunchbox.grating_distance, 0.23)
    yield from scan([lunchbox], servo, 0, 45, 10)
    yield from bps.abs_set(servo, 0.0)


if __name__ == "__main__":
    consumer = Consumer()

    RE = RunEngine()
    RE.subscribe(consumer)
    RE(scan_diffraction(), lambda name, doc: pprint({"name": name, "doc": doc}))

    spot_finder = consumer.spot_finder
    assert spot_finder
    plus_len = len(spot_finder.plus_angles)
    minus_len = len(spot_finder.minus_angles)
    plt.plot(spot_finder.servo_angles[:plus_len], spot_finder.plus_angles, label="+")
    plt.plot(spot_finder.servo_angles[:minus_len], spot_finder.minus_angles, label="-")

    plt.xlabel(r"$\alpha$ (degrees)")
    plt.ylabel(r"$\theta$ (degrees)")

    plt.legend(loc="upper left")
    plt.show()
