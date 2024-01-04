Finding the distance between spots
==================================

This page will walk through how we can take an image and find the distance
between the spots observed in it. 

Starting commit
---------------
::

    git checkout ca60f0ce


Writing a calibration function
------------------------------

There are many ways of calibrating images, but perhaps the simplest is to 
find a red, green or blue object that you know the dimension of, and lean
it against (or stick it onto) the surface onto which your diffraction spots
will appear. You can then take an image of that object, and observe a single
RGB channel to notice how it appears.

For example, you could use a green post-it. In this case, I've picked up an 
old red amazon fire kindle lying around my house and used that. You can take
an image either by running a ``bluesky.plans.count`` plan and inspecting the
``latest_image`` attribute of the ``LunchBox`` device, or by doing the
following::

    from lunchbox.devices.lunchbox import LunchBox
    
    lb = LunchBox(name="lb")
    lb.camera.start()
    image = lb.camera.get()
    lb.camera.stop()

You can then view it with matplotlib::

    import matplotlib.pyplot as plt 
    plt.imshow(image[...,1])
    plt.show()

Which RGB channel you look at will need to be chosen based on the color of
your object. Standard python array images are stored in RGB format so, in the
above code snippet I've selected the green channel, although I have a red object.
This is because I have a reflective white background, so looking at the image
via the red channel ``image[...,0]`` will reveal the whole image as being 
saturated. However, red objects appear red because they completely absorb other
colors, meaning viewing it in the green or blue channels will show their locations
as reflecting none of that light. That is, pixels in these channels will show up
as 0 for that object.

This can be used to work out the area per pixel, as we can simply add up all
the pixels with values of 0 in the green/blue channels, add them up, and divide
the total area of the object by this number to get the area per pixel.

Coding Challenge: Write and integrate a calibration function
------------------------------------------------------------

Modify the ``stage`` method of the ``LunchBox`` so that it takes an initial
image when the laser is off, and uses this to find the area covered by each pixel
in the image, before ``trigger`` is called.

It should use this information to find the distance between spots each time
``trigger`` is called, so that ``read`` reports this distance instead of outputting
the image as an array.

For example, if there are 3 diffraction spots found, the result of ``read`` should be 
an array looking something like::

    [-10, 10]

Where the units might be in centimeters.
