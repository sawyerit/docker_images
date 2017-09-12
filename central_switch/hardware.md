
Central Station - Hardware
======================

Visit the main page for an introduction:
[Central Station v0.1](https://github.com/sawyerit/docker_images/tree/master/central_switch)

Based on this awesome work by Andrew Shilliday Garage Door Controller v1.1

Overview:
---------

Hardware instructions for monitoring your automatic garage doors.  This project will:
* Monitoring of the state of the garage doors (indicating whether they are open, closed, opening, or closing)
* Remote control of the garage doors

In future updates:
* Monitoring man doors of your house
* Controlling lights, cameras or other devices (todo: in a plug and play fashion)

TODO: update these instructions for the changes made in my setup

Harwdare requirements:
-----

**Hardware**

* [Raspberry Pi](http://www.raspberrypi.org)
* [Raspberry Pi Zero W](https://www.adafruit.com/product/3410?gclid=CjwKCAjwuITNBRBFEiwA9N9YEDkpJEFu-aiiTHkML_k4NE2clFAz4Ujuy2McEmUvYHpdlutGi9NEHRoCkR4QAvD_BwE) 
* Micro USB charger (1.5A preferable)
* 8 GB micro SD Cards
* Relay Module, 1 channel per garage door ([SainSmart](http://amzn.com/B0057OC6D8)
* [Magnetic Contact Switches](https://www.amazon.com/Directed-Electronics-8601-Magnetic-Switch/dp/B0009SUF08) (one per door)
* [Jumper wires](http://amzn.com/B007XPSVMY) (or you can just solder)
* 2-conductor electrical wire


Hardware Setup:
------

*Step 1: Install the magnetic contact switches:*

The contact switches are the sensors that the raspberry pi will use to recognize whether the garage doors are open or shut.  You need to install one on each door so that the switch is *closed* when the garage doors are closed.  Attach the end without wire hookups to the door itself, and the other end (the one that wires get attached to) to the frame of the door in such a way that they are next to each other when the garage door is shut.  There can be some space between them, but they should be close and aligned properly, like this:

![Sample closed contact switch][3]

*Step 2: Install the relays:*

The relays are used to mimic a push button being pressed which will in turn cause your garage doors to open and shut.  Each relay channel is wired to the garage door opener identically to and in parallel with the existing push button wiring.  You'll want to consult your model's manual, or experiment with paper clips, but it should be wired somewhere around here:

![!\[Wiring the garage door opener\]][4]
    
*Step 3: Wiring it all together*

The following diagram illustrates how to wire up a two-door controller.  The program can accommodate fewer or additional garage doors (available GPIO pins permitting).

![enter image description here][5]

Note: User [@lamping7](https://github.com/lamping7) has kindly informed me that my wiring schematic is not good.  He warns that the relay should not be powered directly off of the Raspberry Pi.  See his explanation and proposed solution [here](https://github.com/andrewshilliday/garage-door-controller/issues/16).  That being said, I've been running my Raspberry Pi according to the above schematic for years now and I haven't yet fried anything or set fire to my house.  Your milage may vary.

For software instructions go [here](software.md) 

  [1]: http://i.imgur.com/rDx9YIt.png
  [2]: http://i.imgur.com/bfjx9oy.png
  [3]: http://i.imgur.com/vPHx7kF.png
  [4]: http://i.imgur.com/AkNl6FI.jpg
  [5]: http://i.imgur.com/48bpyG0.png
  
