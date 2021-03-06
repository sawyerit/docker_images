
Central Station v0.1 - monitor and control your home from the web w Raspberry Pi.
======================

Based on this awesome work by Andrew Shilliday
[Garage Door Controller v1.1](https://github.com/andrewshilliday/garage-door-controller)



Overview:
---------

This project provides software and hardware installation instructions for monitoring and controlling your house locally or remotely (via the web or a smart phone). The software is designed to run on a [Raspberry Pi](www.raspberrypi.org), and supports:
* Monitoring of the state of the garage doors (indicating whether they are open, closed, opening, or closing)
* Remote control of the garage doors
* Logging of all garage door activity to a Google spreadsheet

In future updates:
* Monitoring man doors of your house
* Controlling lights, cameras or other devices (todo: in a plug and play fashion)

Requirements for monitoring automatic garage doors:
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

**Software**

* [Raspbian](http://www.raspbian.org/)
* Python >2.7 (installed with Raspbian)
* Raspberry Pi GPIO Python libs (installed with Raspbian)
* Python Twisted web module
* Pigpio remote gpio library
* Bootstrap CSS & JQuery
* As a bonus, you can expose the website through a port on your router to access from anywhere!  I personally use [Duck DNS](http://www.duckdns.org) for dynamic dns so I don't have to worry about the ip changing.

[Hardware Setup Instructions](https://github.com/sawyerit/docker_images/tree/master/central_switch/hardware.md)
------


[Software Installation Instructions](https://github.com/sawyerit/docker_images/tree/master/central_switch/software.md)
-----


Nice to have future items:
-----
* Alexa skill to get status of garage door
* enable touchscreen on seperate PI for controlling items
