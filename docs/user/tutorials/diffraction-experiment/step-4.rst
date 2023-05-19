EPICs and pythonSoftIoc
=======================

The pico is connected to the raspberry pi via USB. We can setup a serial
connection to it via python to read and write to it.

At the moment, the script running on the pico just takes a couple of
values and uses them to set the led brightness and servo angle. It does not 
write anything back. This makes our task here a little easier.

Setup a virtual environment
---------------------------
We will now create a virtual envionment and install project dependencies::
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -e .[dev]

For a raspberry pi, some libraries take a while to install (e.g. opencv). Grab 
a coffee...

You will also need to install scikit-image. This isn't supported via pip for
the Raspberry pi OS, so you should run::
    sudo apt-get install python-matplotlib python-numpy python-pil python-scipy
    sudo apt-get install build-essential cython
    pip3 install scikit-image

pythonSoftIOC lets us define software IOCs (or, soft IOCs) with callbacks, so 
we can spin them up and in a terminal call `caget` and `caput` to directly
interact with our devices. In our case, the alternative to this is using vscode
or opening up the serial interface through `minicom`, neither of which we want
to do in a real running experiment. So, an epics layer here is useful.

Boilerplate IOC
---------------

Our use case is quite simple, so we can copy and paste the code in the 
[pythonSoftIoc](https://github.com/dls-controls/pythonSoftIOC) README and only
need to change a couple of things.

Firstly, it makes sense that we should have one IOC with two PV's; one for the
servo and one for the laser. As per the README above, we want to setup a read/
write PV for each of these. From an EPICs perspective, an 'input' is an input
to EPICs from a device. This means we want our output PVs to have callback
functions that write a binary string to our serial connection.

Here is how to setup a serial connection to the pico on python::
    import serial
    tty = serial.Serial("/dev/ttyACM0", 115200)
    tty.write(b"65535 10000\r\n")
    tty.flush()

Note that the serial connection can only pass binary strings, `b""`. They must
end with a carriage return, `\r\n`. Also note that we want two PVs with two
callback functions, yet both of them will need to do something like the above
This means, for example, the led callback function will need to find out what 
the servo value is before writing this string.

Try writing the IOC yourself, and saving this to a file, `src/lunchbox/ioc.py`.
Or, go straight to the next commit.

Checkout the next commit
------------------------

Type the following into a normal terminal::
    git checkout b5cdf5c

You should be able to starup the softIOC and test it works. Do this by typing
the following into a terminal::
    python src/lunchbox/ioc.py

Now, open a new terminal either in vscode or otherwise, and type::
    caget LUNCHBOX:LED
    caput LUNCHBOX:LED 1
    caput LUNCHBOX:SERVO 25
    caget LUNCHBOX:SERVO.RBV

You should see the servo move and the led change brightness.