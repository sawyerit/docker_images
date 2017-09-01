
Central Station - Software
======================

Visit the main page for an introduction:
[Central Station v0.1](https://github.com/sawyerit/docker_images/tree/master/central_switch)




Overview:
---------

Software instructions for monitoring your home:
* Monitoring of the state of the garage doors (indicating whether they are open, closed, opening, or closing)
* Remote control of the garage doors
* Logging of all activity to a google spreadsheet

In future updates:
* Monitoring man doors of your house
* Controlling lights, cameras or other devices (todo: in a plug and play fashion)

Requirements for monitoring automatic garage doors:
-----

* [Raspbian](http://www.raspbian.org/)
* Python >2.7 (installed with Raspbian)
* Raspberry Pi GPIO Python libs (installed with Raspbian)
* Python Twisted web module
* Pigpio remote gpio library
* Bootstrap CSS & JQuery
* Optionally - google drive OAuth key


Software Installation:
-----

_Steps 1 and 2 for both the RPi server and the RPI Zero W controller_

1. **Install [Raspbian](http://www.raspbian.org/) onto your Raspberry Pi**
    1. [Tutorial](http://www.raspberrypi.org/wp-content/uploads/2012/12/quick-start-guide-v1.1.pdf)
    2. [Another tutorial](http://www.andrewmunsell.com/blog/getting-started-raspberry-pi-install-raspbian)
    3.  [And a video](http://www.youtube.com/watch?v=aTQjuDfEGWc)!

2. **Configure your WiFi adapter** (if necessary).
    
    - [Follow this tutorial](http://www.frodebang.com/post/how-to-install-the-edimax-ew-7811un-wifi-adapter-on-the-raspberry-pi)
    - [or this one](http://www.youtube.com/watch?v=oGbDawnqbP4)

    *From here, you'll need to be logged into your RPi (e.g., via SSH).*

3. **RPi Zero W Controller Software**
    - pigpiod should be running as a daemon on the pi
        - Enable remote GPIO with [this tutorial](https://gpiozero.readthedocs.io/en/stable/remote_gpio.html)
        - `$ sudo pigpiod` will run once, but not on reboot
    - Optionally you may remove extraneous application in Raspbian with these commands
        - `$ sudo apt-get purge libreoffice wolfram-engine sonic-pi scratch`
        - `$ sudo apt-get autoremove`


4. **RPi Server Software**

    1. Add Docker to your Pi.  [I used this great tutorial](https://blog.alexellis.io/getting-started-with-docker-on-raspberry-pi/)
    2. Clone or download the [central_switch docker code](https://github.com/sawyerit/docker_images/tree/master/central_switch)
    3. Edit `config.json`
        You'll need one configuration entry for each garage door.  The settings are fairly obvious, but are defined as follows:
        - **name**: The name for the garage door as it will appear on the controller app.
        - **relay_pin**: The GPIO pin connecting the RPi to the relay for that door.
        - **state_pin**: The GPIO pin conneting to the contact switch.
        - **state_pin_closed_value**: The GPIO pin value (0 or 1) that indicates the door is closed. Defaults to 0.
        - **approx_time_to_close**: How long the garage door typically takes to close.
        - **approx_time_to_open**: How long the garage door typically takes to open.
        - **auto_door**: True for automatica garage doors, False for all other doors.  Defaults to False

        The **approx_time_to_XXX** options are not particularly crucial.  They tell the program when to shift from the opening or closing state to the "open" or "closed" state.  You don't need to be out there with a stopwatch and you wont break anything if they are off.  In the worst case, you may end up with a slightly odd behavior when closing the garage door whereby it goes from "closing" to "open" (briefly) and then to "closed" when the sensor detects that the door is actually closed.

        
    4. Build and Run this docker image
        - Build it FROM the central_switch directory: 
            - `$ docker build -t central_switch .`
        - Run it FROM the central_switch directory:
            - `$ docker run --privileged -t --restart unless-stopped -d -v $PWD:/root -p 8000:8000 central_switch`
            - --privleged: To access the GPIO pins the container must be run in priveledged mode.
            - --restart: The container will automatically restart unless manually stopped
            - -v: the container will mount the current dir as a volume and map it to /root on the Pi
        - Other images can be [found here](https://github.com/alexellis/docker-arm/tree/master/images/armv6)
    

Code explanation:
---

**How to use Central_Switch**
todo: explain fundamentals of the idea for central_switch

**Writing logs to google spreadsheet**
`spreadsheet.py` - handles connecting to google drive using oauth setup.
Each logger can specify a spreadsheet tab. (note: tab must exist and all empty rows removed for now)
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html


**Using the Controller Web Service**
todo:
The garage door controller application runs directly from the Raspberry Pi as a web service running on port 8000.  It can be used by directing a web browser (on a PC or mobile device) to http://[hostname-or-ip-address]:8000/.  If you want to connect to the raspberry pi from outside your home network, you will need to establish port forwarding in your modem.  
<br>
When the app is open in your web browser, it should display a home page with an entryfor garages, lights etc. The garage page should show an entry for each "door" configured in your `config.json` file, along with the current status and timestamp from the time the status was last changed.  Click on any entry with `auto_door == True` to open or close the door (each click will behave as if you pressed the garage button once and will optionally log to the google spreadsheet).
