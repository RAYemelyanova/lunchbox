Hardware calibration and the bluesky event model
================================================

In the previous tutorial, you will have encountered how to set up the LunchBox
beamline, both for the hardware and software components to run a basic bluesky
count plan. This tutorial will expand on this, by running more complex bluesky
plans to calibrate the hardware we have.

At the end of the previous tutorial, we were able to take pictures of our camera
showing (hopefully) some diffracted spots in an image. However, lots of questions
remain before we can do an actual diffraction experiment to, for example, estimate
the diffraction grating spacing:

1. What is the physical distance between the diffraction spots in the images?
2. How can we best capture images, without spitting them out as big arrays
   in bluesky documents?
3. Is the diffraction grating perpendicular to the surface on which the spots are
   diffracted? If not, what is the closest position we can get it to, and what
   angle to the surface does this have?

These will be answered in the pages below.


.. grid:: 1 1 1 1
    :gutter: 4

    .. grid-item-card:: :material-regular:`build;2em`

        .. toctree::
            :caption: Finding the distance between spots
            :maxdepth: 1

            distance-between-spots

        +++

       Find the distance between diffraction spots in an image. 
        

    .. grid-item-card:: :material-regular:`swap_horiz;2em`

        .. toctree::
            :caption: Understanding the event model 
            :maxdepth: 1

            event-model
        +++

        Look into the event model to more efficiently emit image data from the 
        camera.

    .. grid-item-card:: :material-regular:`text_snippet;2em`

        .. toctree::
            :caption: Servo calibration
            :maxdepth: 1

            servo-calibration

        +++

        Write an adaptive bluesky plan to calibrate the servo.
    
    .. grid-item-card:: :material-regular:`code;2em`
