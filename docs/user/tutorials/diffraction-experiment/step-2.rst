Connect to the pico
===================

Open the command pallete in vscode and search for 'Pico-W-Go'. Select 
'Pico-W-Go > Configure project'. You should see a popup on the bottom right
telling you the setup was successful. Then, open the command pallete again
and this time search for and select 'Pico-W-Go > Global Settings'. From here,
scroll down to the Sync Folder setting and type::
    src/lunchbox/pico

This will configure the specified folder to sync with the pico. On the bottom
of the vscode window you should see some icons like 'Pico W Connected', 'Run', 
'Reset' and 'All commands'. From now on it is easier to interact with the
Pico-W-Go extension via these buttons. Try it now by clicking the 'Pico W
Connected' button until you see a green tick; you should see a terminal open
stating that it has connected: something like this::
Disconnected
(AutoConnect enabled, ignoring 'manual com port' address setting)
Searching for boards on serial devices...
Connecting to /dev/ttyACM0...

>>> 

This is a terminal directly onto the pico. From here, we can investigate how to
control the LED and the servo through the serial port, first by directly
manipulating these through this terminal, and then by saving a `main.py` file
on the pico which will automatically run whenever the pico is powered.

At the moment, your pico has no files on it. Click on the 'All commands' 
button at the bottom of the screen and select 'Pico-W-Go > Upload Project'. 
You will see the terminal report the status of uploading. If it's being a bit 
slow, pressing enter a few times ought to get it running.

Now, in the micropython terminal, you can type the following::
    >>> from hello import print_hello
    >>> print_hello()
    hello world!
    >>>

Now let's try to control the LED/servo through this connection.