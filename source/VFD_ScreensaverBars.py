#!/usr/bin/python
# -*- coding: utf-8 -*-
import VFD_UI
import VFD_PercentageBar
import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)

if __name__ == '__main__':  
    """This is a small example that demonstrates the function of the Percentage Bar"""
    
    """Define the PRi pins for data communication."""
    VFD_PIN_RS = 27 #A0
    VFD_PIN_EN = 22 #RD
    VFD_PIN_CS = 10 #Chip Select
    VFD_PIN_D0 = 14
    VFD_PIN_D1 = 15
    VFD_PIN_D2 = 18
    VFD_PIN_D3 = 23
    VFD_PIN_D4 = 24
    VFD_PIN_D5 = 25
    VFD_PIN_D6 = 8
    VFD_PIN_D7 = 7
    
    """Create VFD and Percentage Bar Objects"""
    VFD = VFD_UI.Noritake_VFD_UI(VFD_PIN_RS, VFD_PIN_EN, VFD_PIN_CS, VFD_PIN_D0, VFD_PIN_D1, VFD_PIN_D2, VFD_PIN_D3, VFD_PIN_D4, VFD_PIN_D5, VFD_PIN_D6, VFD_PIN_D7)
    Balken =  VFD_PercentageBar.VfdPercentageBar(VFD)
    
    """define timings"""
    sleep_time = 0.02
    pause_time = 0.5
    
    """main loop"""
    while True:
                
        try:
            """randomly generate positions"""
            start= random.randint(1,16)
            stop = random.randint(start+4, 20)
            line = random.randint(0,1)
            
            """set up lenght and position of the Percentge Bar"""
            Balken.set_bar_start(start)
            Balken.set_bar_stop(stop)
            Balken.set_bar_line(line)
            
            """print bar on screen"""
            Balken.setup_bar()
            
            """fill bar until 100%"""
            for i in range(100):
                Balken.update(i+1)
                time.sleep(sleep_time)
                
            """pause"""
            time.sleep(pause_time)
            
            """empty bar until zero"""
            for i in range(100):
                Balken.update(100-(i+1))
                time.sleep(sleep_time)
            
            """remove bar from screen"""
            Balken.clear_bar()
            
        except:
            VFD.clear_display()
            GPIO.cleanup()
                    
    GPIO.cleanup()
