Control the hardware through python
===================================

Both the servo and the LED can be controlled by changing the pulse width
modulation (PWM) duty cycle applied to them. PWM refers to a series of
on/off signals that can be sent to a device, with a time period between
'on' signals referred to as the pulse width. The duty cycle is a number between
0 and 1; 0 means the 'on' signal never comes on, and 1 means the 'on' signal
is always on. 0.5 means, for example, there is an equal amount of 'on' signal
as 'off' signal. The frequency of this signal will determine the behaviour of
the device; an LED driven in this way should have a high frequency. This is
because naturally human eyes struggle to resolve things moving faster than 30
fps; there is a frequency above which our eyes cannot resolve on/off signals
for an LED, and just interpret it as 'on'. As we vary the PWM our eyes
integrate the signal over time, making a higher duty cycle seem brighter than
a lower duty cycle, although in reality the brightness is the same, it's just
modulating really fast.

Starting commit
---------------
::

    git checkout ca60f0ce


Controlling the laser
---------------------

Controlling both the laser and the servo is relatively straightforward,
and is done using the pigpio library. Once installed (if you followed the
instructions from the previous step, you should have a python virtual environment
with this dependency installed) you can do::

    sudo pigpiod

This will start the pigpio daemon. Pigpio means we can use any GPIO pin on
the raspberry pi as a hardware PWM pin. For this tutorial, I've still decided
to use the conventional pins for PWM (GPIO_18 and GPIO_19) however you are
free to use whichever GPIO pins you wish for this.

A script under ``src/lunchbox/pwm.py`` already contains all the code needed
to control the laser. Ensuring you've activated the virtual environment, open 
up a terminal in the root folder of the lunchbox repository, and type::

    from lunchbox.pwm import control_led
    control_led(10000, 100)

You should see the laser turn on. Go ahead and experiment with changing the
frequency and the duty cycle; 100 means 100%, and 0 means 0%. If you get the
frequency low enough you should be able to make out individual pulses.

Controlling the servo
---------------------

As in the previous step, we use the pigpio library to control the servo. Ensure
the daemon is running::

    sudo pigpiod

The ``src/lunchbox/pwm.py`` script contains another function which can be used
to control the servo::

    from lunchbox.pwm import control_servo
    control_servo(500)

This will rotate the servo motor until it has reached a rotation limit. If you
enter 2500, it will rotate the other way, as far as it can.

If you observe your servo as it rotates, you may notice that if your servo has
an arm mounted on to it, it is difficult to tell exactly when a diffraction grating
sitting on this arm is completely perpendicular to an incoming light source. For
this reason, there is another tutorial that takes you through using bluesky to run
an adaptive scan, to calibrate the motor. (TODO: reference this here). For the
moment, just judge by eye roughly where to put the servo arm so it looks 
perpendicular at an input value of 500.

Code Challenge: Make the servo controllable by an angle
-------------------------------------------------------

At the moment, the functions in ``src/lunchbox/pwm.py`` define how a laser can
be controlled by a frequency and a value from 0 to 100, and how a servo can be
controlled using a pulse width (500 to 2500). This is not very easy to translate
to an angle. The goal of this challenge is to:

1. Make the frequency for the laser a little less changeable; in reality we 
probably don't care to change the frequency as often as the duty cycle
2. Adapt the function to control the servo to accept an angle instead of a pulse 
width

For the second point, setting the servo to 0 should set it to 500 pulse width, and
180 should set it to some number that probably sits between 2000 and 2500,
depending on what servo you've got.

Checkout the next commit
------------------------
Type the following into a normal terminal::

    git merge a78818f

Fix the merge conflicts and commit your changes.

Next, we will write an epics layer to interact with the laser and the servo via
channel access.
