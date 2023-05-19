Control the servo and laser
=====================

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

Controlling the laser
---------------------

With this in mind, here is how we can change the duty cycle for our laser::
    >>> from machine import Pin, ADC, PWM
    >>> channel = 0
    >>> frequency = 10000
    >>> pwm_driver = PWM(Pin(channel))
    >>> pwm_driver.freq(frequency)
    >>> pwm_driver.duty_u16(65535)
    >>> pwm_driver.duty_u16(0)

We set a high frequency for our laser, and specify the PWM channel as 0. This
is because on the pinout diagram for the pico, the LED is plugged into the GP0
slot. In case your LED is plugged into any other pin, you will need to change
this number to account for this. Once we created our pwm_driver object with the
correct pin and frequency, we called the `duty_u16` method. `u16` refers to 
unsigned integer, i.e. positive 16 bit integers. These numbers go from 0 to
2**16 -1 (which is 65535). In this case, a duty cycle of 1 means a value of
65535, the largest possible `u16` number, and a duty cycle of 0 is still 0.

Controlling the servo
---------------------

Here is how we can change the duty cycle for the servo::
    >>> channel = 15
    >>> frequency = 50
    >>> pwm_driver = PWM(Pin(channel))
    >>> pwm_driver.freq(frequency)
    >>>
    >>> self.pwm_driver.duty_ns(int(1.0 * 1e6))
    >>> self.pwm_driver.duty_ns(int(0.5 * 1e6))

For this section I recommend you take the servo out of the housing, so that the
diffraction grating can freely rotate without obstruction.

Notice the frequency is much lower, and here we drive the servo with the 
`duty_ns` method instead. Here, the duty cycle is given in terms of the
milliseconds for which the 'on' signal is actually on. Datasheets for servos 
usually mention at which frequency they can be driven, and the angles to which
they rotate will depend on a range of this pulse width. To work it out, you
will need to do some experimenting...

Ensuring the diffraction arm isn't going to hit anything, try driving your 
servo between 0 and 20 ms. 20 is chosen here because at 50 hertz that is the
duration of a pulse (1/50 = 0.02 seconds). Notice when the arm actually 
rotates, and roughly to what angles. Does it go from 0 to 360, or 0 to 180?
Perhaps it goes from 0 to 190. You can decide to 'calibrate' this servo exactly
but for this experiment 0.5 ms to 2.5ms is a good range for 0 to 180 degrees.

Writing a main.py file
----------------------

Now we are going to write a main.py file to let us tell the pico, over a USB
connection, what the laser and the servo should be driven to. You can try doing
this yourself or just skip to the final section of this file to checkout
the next commit to see the result.

Write a file called led.py and another called servo.py. These will contain
python classes or functions that control the led and the servo independently. 
Both these classes/functions should take input parameters to tell them which
pico channel to use, and at what frequency the PWM signals should be driven. 
They should both have 'drive' methods which will drive the device, based on a 
uint16 input - i.e. a number between 0 and 65535. 

Remember for the servo, you will need to define 'mininimum' and 'maximum'
values of the duty cycle that correspond to minimum and maximum angles. 
You can use either the `duty_u16` or `duty_ns` methods, just be consistent
with whichever method you use.

Finally, write a `main.py` file that creates these objects and constantly
listens to input. For this, you will need to use a `while` loop, and the
`input` python function. Remember to upload your project to the pico when you
save.

Note: once you have a main.py, the pico will execute it on restart. To stop,
just hit `Ctrl+C` to interrupt and you can use its terminal again.

Checkout the next commit
------------------------

Type the following into a normal terminal::
    git checkout a78818f


Opening the command pallete or otherwise, upload the project to your pico. This
should sync all files in `src/lunchbox/pico` onto the pico. Connect to the pico
and a terminal should open up that looks a little different::
    Disconnected
    (AutoConnect enabled, ignoring 'manual com port' address setting)
    Searching for boards on serial devices...
    Connecting to /dev/ttyACM0...

    incorrect number of params given. Need 2 (brightness, angle). Restarting...

Try typing in two unsigned integer 16 numbers, like `65535 10000`. You should
see the led turn on to its maximum brightness and the servo should rotate a bit.

Next, we will write an epics layer to interact with the led and the servo via a
regular command line.