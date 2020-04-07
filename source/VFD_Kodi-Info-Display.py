#!/usr/bin/python
# -*- coding: utf-8 -*-
import VFD_UI
import VFD_ScreenBuilder
import Kodi_API_FSM
import RPi.GPIO as GPIO
import time
import configparser
GPIO.setmode(GPIO.BCM)

if __name__ == '__main__':  
    
    """define config destination"""
    iniData = configparser.ConfigParser()
    iniData.read('config.ini', encoding='utf-8')
    
    """get pin setup from ini file"""
    VFD_PIN_RS = int(iniData.get('VFD', 'A0')) #A0 is the equiv to "register select" for HD44780
    VFD_PIN_EN = int(iniData.get('VFD', 'RD')) #RD is the equiv to "enable"
    VFD_PIN_CS = int(iniData.get('VFD', 'CS')) #Chip Select LOW=selected, HIGH=deselected
    VFD_PIN_D0 = int(iniData.get('VFD', 'D0')) #\
    VFD_PIN_D1 = int(iniData.get('VFD', 'D1')) # |
    VFD_PIN_D2 = int(iniData.get('VFD', 'D2')) # |
    VFD_PIN_D3 = int(iniData.get('VFD', 'D3')) # |-- 8 Bit Data Bus
    VFD_PIN_D4 = int(iniData.get('VFD', 'D4')) # |
    VFD_PIN_D5 = int(iniData.get('VFD', 'D5')) # |
    VFD_PIN_D6 = int(iniData.get('VFD', 'D6')) # |
    VFD_PIN_D7 = int(iniData.get('VFD', 'D7')) #/
    
    """initiate Kodi API communication"""    
    Kodi = Kodi_API_FSM.KodiFSM(iniData.get('Kodi', 'IP'))
    
    """initiate VFD display and setup the screen builder"""
    VFD = VFD_UI.Noritake_VFD_UI(VFD_PIN_RS, VFD_PIN_EN, VFD_PIN_CS, VFD_PIN_D0, VFD_PIN_D1, VFD_PIN_D2, VFD_PIN_D3, VFD_PIN_D4, VFD_PIN_D5, VFD_PIN_D6, VFD_PIN_D7)
    Screen = VFD_ScreenBuilder.VFD_ScreenBuilder(VFD, Kodi.state())
    
    """time between Kodi API polls"""
    sleep_time = float(iniData.get('Generic', 'UpdateTime'))
    
    """initial timestamp"""
    next_poll = time.time() + sleep_time
        
    try:
        while True:
            
            """time for next poll?"""
            if time.time() > next_poll:
                
                """setup time for next poll"""
                next_poll = time.time() + sleep_time
                
                """get the current Kodi state"""
                Kodi_state = Kodi.state()
                
                """bring information on screen"""
                Screen.build(Kodi_state)
                
            
    finally:
        VFD.clear_display()
        GPIO.cleanup()
      
