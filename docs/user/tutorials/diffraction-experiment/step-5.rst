Ophyd devices
=============

Now we have a working EPICs IOC, we can combine it with the pi camera to 
complete the hardware abstraction for our experiment. We should start by
writing a device for the camera.

Programmatically, an ophyd device is a class that inherits from an ophyd
Device (or a child of this class) which needs to obey certain protocols
to be used in bluesky plans. For now, we can write a simple device which
is just going to be used in another device, so it doesn't need much 
boilerplate.

Taking pictures with the pi camera
----------------------------------
you can take an image with the pi camera to check it's working via the
command line::
    raspistill -t 5 -o image.jpeg

This should show you the camera output for 5 seconds before taking and saving 
a picture under `image.jpeg`. 

In python, you can do::
    from picamera import PiCamera
    camera = PiCamera(resolution=(500, 100))
    camera.start_preview()
    camera.stop_preview()
    camera.close()

Calling `camera.start_preview()` will open up a preview that could cover 
part of your screen. Hopefully you'll still be able to see your terminal 
to type the next line which will close it.

Making ophyd devices
--------------------
By inheriting from an ophyd.SignalRO Device, we can make an ophyd device to 
define this camera. This class will need a `get` method so we can take
pictures, a `create` method to create the camera and a `delete` method to free
up the memory it uses, by calling `camera.close()`. 

Then, we can define an ophyd device that encapsulates this camera, as well as 
the led and servo that we have exposed through the EPICs PVs; `LUNCHBOX:SERVO`
and `LUNCHBOX:LED`.

There are several bluesky protocols that can be implemented on ophyd devices in
order that they can be used for bluesky plans. For example, a 'Readable' device
will have a `read` and `describe` method, a 'Stageable' will have a `stage` and
`unstage` method, and a 'Triggerable' has a `trigger` method. All bluesky 
protocols are listed [here](
    https://github.com/bluesky/bluesky/blob/master/bluesky/protocols.py).

Stageable devices will always have their `stage` and `unstage` methods called
before and after each bluesky plan has run.

Try to write two ophyd devices; one for the pi camera, and one for the entire
setup, i.e. encapsulating the camera, led and servo. The latter should be
Readable and Stageable for now. We want to call bluesky.plans.count on this
device (see (here)[https://blueskyproject.io/bluesky/generated/bluesky.plans.count.html#bluesky.plans.count]
for documentation) with `num=1`, which will call `stage`, `read` and `unstage`.
This will also call the `describe` method to generate bluesky documents.
For now, we will not focus much on what bluesky documents are; they are blobs
of JSON that can contain some results of our experiment. What results they
contain is the job of the `describe` method to dictate.

Make sure to call the camera's 'create' and 'delete' methods in the stage
and unstage methods of the lunchbox device, as picamera uses ram to 
instantiate.

Once you've had enough, checkout the next commit...

Checkout the next commit
------------------------

Type the following into a normal terminal::
    git checkout 62037e6

(note: you will have to do do pip install -e .[dev] again...)
First, setup the servo at some angle::
    caput LUNCHBOX:SERVO 30.0

If this doesn't work, check your softIOC is running. Now, open up a python 
terminal and type the following::
    from lunchbox.devices import LunchBox
    from bluesky import RunEngine
    from bluesky.plans import count
    import pprint

    RE = RunEngine()

    lunchbox = LunchBox(name="lunchbox")

    RE(count([lunchbox], num=1), lambda name, doc: pprint.pprint({"name": name, "doc": doc}))

You should see the servo move back to 0 degrees, and the led flicker on, and
some documents emitted to the terminal. One of them will have a large array;
this is the array containing the pi camera RGB image when the laser was on.

Congratulations - you have run your first bluesky experiment!