Tutorials
=========

This documentation is for users wishing to learn more about the whole software
stack which will (eventually) replace GDA at Diamond. It is split into 3 main
sections. One of the tutorials exclusively covers the hardware and low-level
software required for experiments to be run on the Lunchbox beamline.
All the other tutorials cover experiments in increasing complexity, introducing
higher level concepts as we go.


Users are encouraged to fork the lunchbox repo from Github, and follow along
each tutorial by checking out the commits mentioned at the start of each page.
By the bottom of the page, they should be able to merge the next commit and deal
with any merge conflicts, thereby checking their answers. Users are welcome to use
their own solution in preference to that provided if they so wish, to continue
the tutorial.


.. grid:: 1 1 1 1
    :gutter: 4

    .. grid-item-card:: :material-regular:`build;2em`

        .. toctree::
            :caption: Hardware and low-level software
            :maxdepth: 1

            set-up/index.rst

        +++

        Setup the hardware and configure it for use by low-level software for 
        the other tutorials.

    .. grid-item-card:: :material-regular:`swap_horiz;2em`

        .. toctree::
            :caption: Hardware calibration and the bluesky event model
            :maxdepth: 1

            calibrate/index.rst

        +++

        Write bluesky plans to calibrate the hardware, running adaptive-scans
        in the process.

    .. grid-item-card:: :material-regular:`text_snippet;2em`

        .. toctree::
            :caption: Diffraction experiment
            :maxdepth: 1

            diffraction-experiment/index.rst

        +++

        Write a bluesky plan which performs a diffraction experiment, and uses
        spot-finding to figure out the resolution of the diffraction grating used.
    
    .. grid-item-card:: :material-regular:`code;2em`
