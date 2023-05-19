Setup
=====


Hardware and Equipment
----------------------

For this tutorial, you will need the following hardware:
1. Raspberry pi - any model will do, so long as it has a slot for a pi 
camera.
2. Raspberry pi pico with soldered pins,
3. Breadboard,
4. Raspberry pi camera,
5. DC Servo motor,
6. Diffraction grating,
6. A 3.3v laser,
7. cables for the raspberry pi camera and breadboard connections,
8. (optional) housing for the experiment

The pi requires a SD card to run, with an operating system (OS) booted onto it. 
You can use any OS, but for this tutorial it is reccomended to use [Raspberry 
Pi OS](https://www.raspberrypi.com/software/); you will need to download 
software for this aim. You can use any distribution, but I used a 32 bit OS.

The raspberry pi pico, or just pico from now on, will need to be booted with
micropython for this tutorial - [official documentation on this exists
](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
, however the link to download the UF2 file may not be the most up-to-date. 
Refer to the [official micropython website]
(https://micropython.org/download/rp2-pico/) to get the latest download file
for the firmware you will need.

Now you are ready to connect the hardware components by following the 
instructions in the how-to/setup-hardware page.

Setting up the pi
-----------------

Go ahead and boot up the raspberry pi. Connect a display to it via the HDMI
cable, and a keyboard and a mouse. Connect the pi to wifi (I used DLS-Visitor)
and open up a terminal.

Checkout this repository onto a folder somewhere on your system::
    cd ~
    git checkout https://github.com/RAYemelyanova/lunchbox.git

[Install vscode] (https://code.visualstudio.com/docs/setup/raspberry-pi)
onto your pi::
    sudo apt update
    sudo apt install code


You don't have to use vscode, but it is a convenient IDE that I like to use for
all aspects of the tutorial, from integrating with the pico to running the
experiments. Once you've installed vscode, ::
    cd lunchbox
    code .

This will open up vscode from the lunchbox folder, which already has some
configurations for vscode. You will see some popus; ignore them for now. 
Throughout this tutorial we will use vscode a lot - it has an inbuilt terminal
that has the same permissions as your regular terminal, a debugger, linting for
the code you write and an extension that lets us write and upload code to the
pico. Often I will ask you to open the command pallete, which is done via the
shortcut (Ctrl+Shift+P) or by navigating to the top bar and clicking `View ->
Command Pallete...`

Try it now. Open the command pallete and search for 'extensions'. Click on
'Configure Recommended Extensions (Workspace Folder)'. vscode has plugins, or
extensions, which extend its functionality. We will be using an extension called
Pico-W-Go which connects to our pico - this will let us edit files on the pi
and copy them to the pico directly. If you'd rather not do this, or you don't
want to use vscode, you can use Thonny instead. Thonny comes packaged into the 
Raspberry Pi OS as the default IDE, and there are lots of guides online on how
to connect to the pico using it.

Checking out the earliest commit
--------------------------------

At the moment, you should be inside a project that has the latest version of 
the lunchbox repo; this tutorial will take you through previous commits of it.
Go ahead and type::
    git checkout ca60f0ce

This will take you to the earliest stage of the repository; at this point, we 
have a file in src/lunchbox/pico that just defines a function to print
'hello world!'.


Now, let's see how we can connect to the pico via vscode.