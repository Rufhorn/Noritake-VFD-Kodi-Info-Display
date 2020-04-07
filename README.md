# Noritake-VFD-Kodi-Info-Display
This project is about attaching a Noritake VFD character display to a Raspberry Pi and print basic player information given by a Kodi media center in your local network.

## Background:
For quite some time I use a Raspberry Pi 3 driven Kodi media center for playing videos and streaming music from a local hard drive as well as from the internet (e.g. radio). The Pi is attached to a AV-receiver unit which, in turn, is attached to my TV. Therefore music can be played by keeping the TV switched off, but every time I want to change the music source I would have to turn on the TV and turn it off again. In order to avoid this I wanted to attach a small character display to the Pi, that prints the current selection and some basic playing information like the title and a progression bar.

## The Display:
The display is a Noritake VFD dot character module of the series CU20026SCPB-KS20AB-05 that I got as a gift some time ago. It only provides 8 bit parallel data communication and the command structure differs from the typical Hitachi HD44780 controls. 
I connected all the lines directly to the Pi’s GPIO, the /WR pin is directly hardware connected to GND (write mode only) in order to protect the Pi’s input since the display runs on 5V logic. The power is drawn from the GPIO as well, but the 320mA the display needs are a little bit borderline and the Voltage drops to the minimum supported by the display.
The concrete pin setup can be defined in the config file. 

## Kodi communication:
Kodi provides a JSON-RPC API that allows to communicate through http requests. Within this project I use preset requests that I collected in a separate file. In general, the JSON RPC gives a lot of possibilities for requesting data from Kodi and even control it remotely.

## Info on Display:
The information printed on screen is customized to my needs. My character display has two lines, the fist is used to print the audio/video title if Kodi is playing anything and the screen selection otherwise. On the second line I just print the system time if nothing is playing or the audio/video supplies no progression state (as it is the case for live streaming content). Otherwise a progression bar is plotted on the full line.
This section is kind of a playground for different things that could be printed as additional information later on.

<p align="center"><img src="/images/photo5206703396432751974.jpg" width="50%">
  
<p align="center"><img src="/images/photo5206703396432751972.jpg" width="50%">


## Final Words:
This project is not just “ready to use”, moreover it is meant to be an example for others who want to create their own custom display. Also I do not claim awards for best coding, I tried to write as clearly as possible for others to make it easy to read.
If you have a similar display and a similar application in mind, feel free to download and modify. ;-)
