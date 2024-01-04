Build the beamline
==================


Congratulations! 🎉 You've just got some components for a lunchbox beamline from Chris Colbourne
and you're ready to get started with building the beamline and running an experiment on it. But
first, please check you have the following parts ⚙️ (and if you're missing one, speak to Chris)


Parts List
----------

+---------------------------------------+----------+
| Item                                  | Quantity | 
+---------------------------------------+----------+
| Raspberry Pi (v4)                     | 1        |
+---------------------------------------+----------+
| Raspberry Pi Power Supply (USB/USB-C) | 1        |
+---------------------------------------+----------+
| Raspberry Pi Pico                     | 1        |
+---------------------------------------+----------+
| Raspberry Pi Camera (v2 onwards)      | 1        |
+---------------------------------------+----------+
| 5V DC Servo Motor                     | 1        |
+---------------------------------------+----------+
| 300 lines/mm diffraction grating      | 1        |
+---------------------------------------+----------+
| 3.3V laser                            | 1        |
+---------------------------------------+----------+
| Breadboard                            | 1        |
+---------------------------------------+----------+
| jumper wires                          | many     |
+---------------------------------------+----------+
| experiment housing (camera and servo) | 1        |
+---------------------------------------+----------+
| mini HDMI to HDMI cable               | 1        |
+---------------------------------------+----------+
| micro USB to USB cable                | 1        |
+---------------------------------------+----------+
| transistor for laser                  | 1        |
+---------------------------------------+----------+
| blue-tac or similar                   | n/a      |
+---------------------------------------+----------+
| A3 sheet                              | n/a      |
+---------------------------------------+----------+
| green post it note                    | n/a      |
+---------------------------------------+----------+
| 32GB+ microSD Card                    | n/a      |
+---------------------------------------+----------+


If you can't find a green post it note, just grab a regular one and run some 
green highlighter over it.

You will also need a stable internet connection, and the ability to write to an
SD card, such as an SD card slot (or adapter) connected to a computer.

Getting started with the Pi
---------------------------
Connecting to the pi requires plugging in the USB/USB-C power supply (depending on
which pi model you have), booting it up with an Operating System (OS) installed on
a microSD card and interfacing with it. The interface can either be physical, by 
plugging in peripherals and a monitor, or virtual.

Physical interface
^^^^^^^^^^^^^^^^^^
To physically interface with the pi, from a machine with a stable internet connection:
1. Install the `pi imager`_ from the official website
2. Launch the imager and install the Raspberry Pi OS (32-bit) for your raspberry pi version onto a microSD card with at least 32GB on it. You don't need to edit settings.
3. Once finished, transfer the microSD to the pi, connect your peripherals and start the device by connecting it to the power supply.

Virtual interface
^^^^^^^^^^^^^^^^^
The physical interface can be annoying because it dedicates peripherals to the pi.
Unless you have some equivalent to a KVM switch setup which can navigate between
your local machine and your pi (or, you have unused peripherals lying around and
the space to use them) this can be space and time consuming. You can do a `headless
setup`_ of the raspberry pi instead. Note that this will not work if you are on the
eduroam wifi, so if you are working at diamond you could try

To get connected to the pi, you need to plug in the USB or USB-C power supply.
Then, you can either plug in peripherals and a monitor, or you can do a headless 
setup where you virtually connect to the pi over a local wifi network. Regardless 
of whichever option you go with, you will need the 
`pi imager`_ to install the Raspbian OS onto an SD card which will get loaded each
time the pi boots up. Since the pi lacks any onboard storage, this SD card will be
where all of your work on the pi gets saved.

Configuring the Pi and Pico
----------------------------
Please follow the `official documentation 
<https://www.raspberrypi.com/documentation/computers/getting-started.html>`_
to install the 32x raspbian OS onto the raspberry pi. 

The raspberry pi pico, or just pico from now on, will need to be booted with
micropython for this tutorial - `official documentation on this exists 
<https://www.raspberrypi.com/documentation/microcontrollers/micropython.html>`_, 
however the link to download the UF2 file may not be the most up-to-date. 
Refer to the `official micropython website 
<https://micropython.org/download/rp2-pico/>`_ to get the latest download file
for the firmware you need.

Installing software on the Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After writing to the SD card, boot up the raspberry pi and connect it to 
peripherals (screen, mouse and keyboard)

^^^^ for subsubsections
"""" for paragraphs apparently.


.. _`pi imager`: https://www.raspberrypi.com/software/

.. _`headless setup`: https://www.hackster.io/435738/how-to-setup-your-raspberry-pi-headless-8a905f#toc-1--installing-raspberry-pi-os-to-sd-card-0
