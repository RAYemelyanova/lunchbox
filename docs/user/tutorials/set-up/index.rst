Hardware and low-level software
===============================

This tutorial guides users through how to configure their hardware with the
raspberry pi, and connect it to low-level software such as EPICs and Ophyd.


.. grid:: 1 1 1 1
    :gutter: 4

    .. grid-item-card:: :material-regular:`build;2em`

        .. toctree::
            :caption: Setup hardware and software
            :maxdepth: 1

            setup-hardware-and-software

        +++

        Setup the hardware and install required software on the pi

    .. grid-item-card:: :material-regular:`swap_horiz;2em`

        .. toctree::
            :caption: Control the hardware through python
            :maxdepth: 1

            python-control-hardware

        +++

        Control the laser and servo using PWM (Pulse Width Modulation)

    .. grid-item-card:: :material-regular:`text_snippet;2em`

        .. toctree::
            :caption: EPICs
            :maxdepth: 1

            epics-abstraction

        +++

        write IOCs for the servo and laser to control them via EPICs caput/caget commands

    
    .. grid-item-card:: :material-regular:`code;2em`

        .. toctree::
            :caption: Ophyd devices
            :maxdepth: 1

            ophyd-devices

        +++

        Define Ophyd devices to connect to the EPICs layer

Once you are finished here, move on to calibration tutorial.
