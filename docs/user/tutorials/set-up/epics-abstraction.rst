EPICs
=====

EPICs defines a protocol to interact with hardware via channel access. We can
configure Input-Output Controllers (IOCs) which have various Process Variables
(PVs). These PVs can be retrieved with ``caget`` and set with ``caput`` via
channel access.

We will be using pythonSoftIoc to set up an IOC that defines PVs for the brightness
of the laser, and the angle of the servo.

pythonSoftIOC lets us define software IOCs (or, soft IOCs) with callbacks. In 
our case, you might be thinking "what's the point, we can control our devices 
through python anyways". You would be right: we don't need to use the EPICS, as
our hardware layer is already written in python. However lots of other bits of
hardware, on real beamlines, is not so easy to control and may be behind a 
network or proxy. pythonSoftIOC therefore lets us communicate directly with 
devices and hide away such complexity.

To see this complexity in action, one could imagine having the laser and servo
signal being connected to a raspberry pi pico, which connects to the Pi
over a USB connection. In this case, it is not so trivial to control the laser
and servo because this requires sending binary strings over the USB connection.
For such a use case, pythonSoftIoc provides an ideal abstraction layer.

Starting commit
---------------
::

    git checkout ca60f0ce

Boilerplate IOC
---------------

Our use case is quite simple, so we can copy and paste the code in the 
[pythonSoftIoc](https://github.com/dls-controls/pythonSoftIOC) README and only
need to change a couple of things.

Firstly, it makes sense that we should have one IOC with two PV's; one for the
servo and one for the laser. As per the README above, we want to setup a read/
write PV for each of these. From an EPICs perspective, an 'input' is an input
to EPICs from a device. This means we want our output PVs to have callback
functions that manipulate the ``Servo`` and ``Laser`` python objects from the
previous stage of the tutorial.

Code Challenge: Write the python soft IOC
-----------------------------------------
Copy and paste the README in the link above, and modify it to attempt setting
up a softIOC containing 4 PVs:
1. LASER:RBV
2. LASER
3. SERVO:RBV
4. SERVO

1 and 3 are readback values, meaning they are equivalent to EPICs aIn records.
The other two are equivalent, therefore, to EPICs aOut records. Save this ioc
file in the location ``src/lunchbox/ioc.py``.

Checkout the next commit
------------------------

Type the following into a normal terminal::

    git merge b5cdf5c

Fix the merge conflicts and commit your changes.

You should be able to starup the softIOC and test it works. Do this by typing
the following into a terminal (ensuring your virtual env is activated)::

    python src/lunchbox/ioc.py

Now, open a new terminal And type::

    caget LUNCHBOX:LED
    caput LUNCHBOX:LED 100
    caput LUNCHBOX:SERVO 25
    caget LUNCHBOX:SERVO.RBV

You should see the servo move and the led change brightness.
