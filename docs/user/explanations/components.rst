Lunchbox structure
==========================

This is what makes up a lunchbox beamline:
1. raspberry pi
2. pi camera v2
3. raspberry pi pico
4. servo motor
5. 3.3v laser (class II)

These components, together with layers of software, explain the structure of
the lunchbox both in its composition and codebase.

Hardware
--------

The pico is primarily used for PWM signals to be sent to the laser, to control
its brightness. It is also used to control the angle of the servo. The 
raspberry pi camera plugs directly into the raspberry pi, on which all future
processing can be done (even if sometimes a bit slowly...). 

The pico can be booted with micropython, a lightweight implementation of python
that runs on microcontrollers, which will look for a `main.py` file on the pico
and run it on startup. The pico is connected to the raspberry pi via USB, over
which it can accept binary strings to execute commands. For this reason, in the
final product of this lunchbox, the `main.py` file continually waits for input
and alters the laser brightness / servo angle in response. This python file is
meant to simulate hardware stimuli in the real-world.


EPICs
-----

EPICs exposes the ways by which the servo and laser states are altered via
`caget` and `caput` calls. This is done through the help of `pythonSoftIoc`,
which sets up callback functions that run on any such calls.


Ophyd
-----

Ophyd acts as a python abstraction layer for all the hardware involved in the
experiment. As an example, the pico controls the laser and led, which is
exposed to a user via an EPICs layer. However, the camera is not. A single
ophyd device can be written which describes how hardware ought to
behave during collection. For example, here, "collection" refers to the pi
camera taking pictures of diffraction spots. For that to happen, we need to
define where those images might be saved, or expose how we could change
the resolution or exposure time of the camera. We may also want to couple
this with the laser, such that the laser turns on automatically for any
images that are taken.


Bluesky
-------
bluesky plans can be written to coordinate an experiment. This can involve 
setting up the correct parameters for ophyd devices (e.g. where you want to
save your images) as well as exactly what you're scanning. The final stage
of this project scans the servo in 5 degree intervals from 0 to 45 degrees,
taking pictures at each interval and turning the led on and off to get
background pictures also.


