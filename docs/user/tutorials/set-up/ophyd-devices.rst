Ophyd devices
=============

Now we have a working EPICs IOC, we can combine it with the pi camera to 
complete the hardware abstraction for our experiment. We should start by
writing a device for the camera.

An ophyd device is written as a class that inherits from ``ophyd.Device``
which needs to obey certain protocols to be used in bluesky plans. 
For now, we can write a simple device which is just going to be used in 
another device, so it doesn't need much boilerplate.

Starting commit
---------------
::

    git checkout ca60f0ce

Taking pictures with the pi camera
----------------------------------
you can take an image with the pi camera to check it's working via the command
line. Assuming you are using the latest "Bullseye" release of Raspberry Pi OS
you can use libcamera to take photos and videos. First, check that the
libcamera is working - it should have come packaged into any official Bullseye
image::

    rpicam-hello

You can take pictures using the ``libcamera-jpeg`` CLI command::

    libcamera-jpeg -o image.jpg -t 5000
    
This should show you the camera output for 5 seconds before taking and saving a
picture under ``image.jpeg``. If you struggle at this stage please refer to the
`Raspberry Pi camera documentation`_.

Earlier in this tutorial we installed picamera2, which should allow us to
control the camera in python. Throughout the rest of this tutorial, if you
struggle to control the camera in python please refer to the 
`Picamera2 manual`_.

In a python command line, you can type the following to turn the camera on::

    from picamera2 import Picamera2, preview

    camera = Picamera2()
    camera_config = picam2.create_preview_configuration()
    camera.configure(camera_config)
    camera.start_preview(Preview.QTGL)
    camera.start()

You should now see a screen showing the camera preview. You may notice it looks
a bit zoomed in, or poor resolution; this is all down to the camera
configuration which can be changed for the ideal set up.

Configuring the pi camera
-------------------------

The `Picamera2 manual`_ contains documentation explaining how the camera
configuration works. There are lots of configurational settings we can change
on the camera - these are camera settings that we cannot change at runtime.
Camera controls can be set during runtime. ``picamera2`` lets us set both
before the camera even turns on, which is useful if we already know what we want.
Otherwise, you can adjust camera controls while looking at a preview::

    camera = Picamera2()
    camera_config = picam2.create_preview_configuration()
    camera.configure(camera_config)
    camera.start_preview(Preview.QTGL)
    camera.start()
    camera.set_controls({"ExposureTime": 100000})

You can use ``camera.camera_controls`` to view a dictionary of all available
controls with a corresponding ``(minimum_value, maximum_value, default_value)``
tuple stored as the value for each key. Some of these will change dynamically
as you alter settings; for example, setting the ``NoiseReductionMode`` of the
camera to ``2`` (corresponding to ``NoiseReductionModeEnum.HighQuality``), will
change the ``FrameDurationLimits`` tuple; that is, the minimum time that the
sensor can take to deliver a frame will increase due to the increased
processing for high quality noise reduction.


Making ophyd devices
--------------------

Ophyd devices are just classes that inherit from ``Ophyd.Device``, which themselves
contain ``Ophyd.signal.Component`` objects that define an interface to soft signals
or underlying EPICs devices. For example, to write a simple Ophyd Device containing
both the laser and the servo we could have::

    from ophyd import Device, EpicsSignal, Component

    class LunchBox(Device):
        laser = Component(EpicsSignal, "LUNCHBOX:LASER")
        servo = Component(EpicsSignal, "LUNCHBOX:SERVO")

From such a class, both the laser and servo can be accessed. Their epics values can
be read and set using the ``.get`` and ``.set` methods on an ``ophyd.EpicsSignal``.

Ophyd devices can be written in whatever way, with any amount of methods just like
regular python classes. However to use bluesky plans (which lets us run complex,
modular scans of our hardware) we need the underlying Ophyd devices to obey
certain protocols. This is because bluesky plans are just a generated list of commands
sent to the RunEngine, which will try and call methods on the Ophyd device such as 
``stage`` and ``unstage``. If these do not exist on the object, we will see an error.

There are several `bluesky protocols`_ that can be implemented on ophyd devices in
order that they can be used for bluesky plans. For example, a 'Readable' device
will have a ``read`` and ``describe`` method, a 'Stageable' will have a ``stage`` and
``unstage`` method, and a 'Triggerable' has a ``trigger`` method.

Stageable devices will always have their ``stage`` and ``unstage`` methods called
before and after each bluesky plan has run.


Coding challenge: Write an ophyd device
---------------------------------------
Try to write an Ophyd device to encapsulate a simple working of the lunchbox beamline.
That is, we want to have a device that, when ``trigger`` is called, takes a picture.
To ensure efficiency and safety, the laser should only be turned on just before the
picture is taken, and should be turned off just after.

This device should be ``Stageable``, ``Readable`` and ``Triggerable``.

Define a ``Camera`` class (which inherits from) ``ophyd.SignalRO`` which manages the
camera state using the above information. Because ophyd component constructors can 
be called multiple times, ensure commands like ``Picamera2()`` are *not* called in 
the constructor, but in another method like ``create()`` or ``start()``. This is 
because picamera can only deal with one handler for the actual camera; if you try 
typing into a terminal ::

    picamera2()
    picamera2()

... you will see an error describing this. Then, in the corresponding ``LunchBox`` device,
you should have something like::

    class Camera(Device):
        camera = Component(Camera, *args, **kwargs)

...where ``args`` and ``kwargs`` are optional positional and keyword arguments that
``Camera`` requires in the constructor. It is recommended for the constructor
to take no arguments.


Checkout the next commit
------------------------

Type the following into a normal terminal::

    git checkout 62037e6

Open up a python terminal and type the following::

    from lunchbox.devices.lunchbox import LunchBox
    from bluesky import RunEngine
    from bluesky.plans import count
    import pprint

    RE = RunEngine()

    lunchbox = LunchBox(name="lunchbox")

    RE(count([lunchbox], num=1), lambda name, doc: pprint.pprint({"name": name, "doc": doc}))

You should see the servo move back to 0 degrees, and the led flicker on, and
some documents emitted to the terminal. One of them will have a large array;
this is the array containing the pi camera RGB image when the laser was on.

You can inspect it by looking at the ``latest_image`` attribute of the ``lunchbox``::

    import matplotlib.pyplot as plt
    plt.imshow(lunchbox.latest_image)
    plt.show()

Congratulations - you have run your first bluesky experiment!


.. _bluesky protocols: https://github.com/bluesky/bluesky/blob/master/bluesky/protocols.py
.. _bluesky.plans.count: https://blueskyproject.io/bluesky/generated/bluesky.plans.count.html#bluesky.plans.count
.. _Raspberry Pi camera documentation: https://www.raspberrypi.com/documentation/accessories/camera.html#installing-a-raspberry-pi-camera
.. _Picamera2 manual: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
