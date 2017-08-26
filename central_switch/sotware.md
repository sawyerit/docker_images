
Central Station - Software
======================

Visit the main page for an introduction:
[Central Station v0.1](https://github.com/sawyerit/docker_images/tree/master/central_switch)




Overview:
---------

Software instructions for monitoring your home:
* Monitoring of the state of the garage doors (indicating whether they are open, closed, opening, or closing)
* Remote control of the garage doors
* Logging of all garage door activity (todo: via ifttt to google sheet??)

In future updates:
* Monitoring man doors of your house
* Controlling lights, cameras or other devices (todo: in a plug and play fashion)

Requirements for monitoring automatic garage doors:
-----

**Software**

* [Raspbian](http://www.raspbian.org/)
* Python >2.7 (installed with Raspbian)
* Raspberry Pi GPIO Python libs (installed with Raspbian)
* Python Twisted web module
* Pigpio remote gpio library
* Bootstrap CSS & JQuery


Software Installation: (todo)
-----

1. **Install [Raspbian](http://www.raspbian.org/) onto your Raspberry Pi**
    1. [Tutorial](http://www.raspberrypi.org/wp-content/uploads/2012/12/quick-start-guide-v1.1.pdf)
    2. [Another tutorial](http://www.andrewmunsell.com/blog/getting-started-raspberry-pi-install-raspbian)
    3.  [And a video](http://www.youtube.com/watch?v=aTQjuDfEGWc)!

2. **Configure your WiFi adapter** (if necessary).
    
    - [Follow this tutorial](http://www.frodebang.com/post/how-to-install-the-edimax-ew-7811un-wifi-adapter-on-the-raspberry-pi)
    - [or this one](http://www.youtube.com/watch?v=oGbDawnqbP4)

    *From here, you'll need to be logged into your RPi (e.g., via SSH).*

3. **Install the python twisted module** (used to stand up the web server):

    `sudo apt-get install python-twisted`
    
4. **Install the controller application**
        
    I just install it to ~/pi/garage-door-controller.  You can install it anywhere you want but make sure to adapt these instructions accordingly. You can obtain the code via SVN by executing the following:
    
    `sudo apt-get install subversion`

    `svn co https://github.com/andrewshilliday/garage-door-controller/trunk ~pi/garage-door-controller`
    
    That's it; you don't need to build anything.

5.  **Edit `config.json`**
    
    You'll need one configuration entry for each garage door.  The settings are fairly obvious, but are defined as follows:
    - **name**: The name for the garage door as it will appear on the controller app.
    - **relay_pin**: The GPIO pin connecting the RPi to the relay for that door.
    - **state_pin**: The GPIO pin conneting to the contact switch.
    - **state_pin_closed_value**: The GPIO pin value (0 or 1) that indicates the door is closed. Defaults to 0.
    - **approx_time_to_close**: How long the garage door typically takes to close.
    - **approx_time_to_open**: How long the garage door typically takes to open.

    The **approx_time_to_XXX** options are not particularly crucial.  They tell the program when to shift from the opening or closing state to the "open" or "closed" state.  You don't need to be out there with a stopwatch and you wont break anything if they are off.  In the worst case, you may end up with a slightly odd behavior when closing the garage door whereby it goes from "closing" to "open" (briefly) and then to "closed" when the sensor detects that the door is actually closed.

        
6.  **Set to launch at startup**

    Simply add the following line to your /etc/rc.local file, just above the call to `exit 0`:
    
    `(cd ~pi/garage-door-controller; python controller.py)&`
    
7. **Using the Controller Web Service**
The garage door controller application runs directly from the Raspberry Pi as a web service running on port 8080.  It can be used by directing a web browser (on a PC or mobile device) to http://[hostname-or-ip-address]:8080/.  If you want to connect to the raspberry pi from outside your home network, you will need to establish port forwarding in your cable modem.  
<br>
When the app is open in your web browser, it should display one entry for each garage door configured in your `config.json` file, along with the current status and timestamp from the time the status was last changed.  Click on any entry to open or close the door (each click will behave as if you pressed the garage button once).
