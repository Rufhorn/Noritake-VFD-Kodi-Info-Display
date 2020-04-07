#!/usr/bin/python
# -*- coding: utf-8 -*-
import VFD_PercentageBar
import VFD_UI
from datetime import datetime

class VFD_ScreenBuilder(object):
    """Setup a custom Screen Print."""
    
    def __init__(self, VFD:VFD_UI.Noritake_VFD_UI, Kodi_state_init:dict):  
        """Needs the VFD object to print the data at and an initial Kodi
        State for reference. Returns nothing."""      
        
        """setup VFD and percentage bar"""
        self._VFD = VFD
        self._Bar = VFD_PercentageBar.VfdPercentageBar(self._VFD)
        
        """clear the two lines of the display"""
        self._VFD.vfd_clear_section(line=0, clear_start=1, length=20)
        self._VFD.vfd_clear_section(line=1, clear_start=1, length=20)
        
        """setup kodi states"""
        self._Kodi_state = {}
        self._Kodi_state_old = Kodi_state_init
        
        """this is a custom offset for the %, otherwise 100% would never
        be printed on screen since Kodi stops playing and prints the
        current selection + removes the percentage bar."""
        self._percentage_offset = 4.0        

    def build(self, Kodi_state):
        """build the screen print"""
        
        """get new state"""
        self._Kodi_state = Kodi_state
        
        """figure out whether to print %Bar or not."""
        self._bar_or_no_bar(self._Kodi_state['percentage'])
        
        """clear display before new print"""
        if self._Kodi_state['title'] != self._Kodi_state_old['title']:
            self._VFD.vfd_clear_section(line=0, clear_start=1, length=20)
            print('New '+self._Kodi_state['type']+': '+self._Kodi_state['title'])
        
        """bring print on screen"""
        self._VFD.vfd_print(self._Kodi_state['title'], alignment='c', line=0)
        
        """save the current state"""
        self._Kodi_state_old = self._Kodi_state
                
    def _bar_or_no_bar(self, current_percentage):
        """use the returned percentage information to decide wheter to 
        print a %Bar on screen or not."""
        switcher = {
            0: self._bar_off,
            0.0: self._bar_off
        }
        # Get the function from switcher dictionary
        func = switcher.get(current_percentage, self._bar_on)
        # Execute the function
        func()
        
    def _bar_on(self):
        """if %Bar has to be printed, figure out whether the bar is 
        already existing."""
        switcher = {
            False: self._Bar.setup_bar,     #%Bar doesn't exist yet
            True: self._bar_update          #%Bar already exists, has to be updated
        }
        # Get the function from switcher dictionary
        func = switcher[self._Bar.get_bar_state()]
        # Execute the function
        func()
        #print('Switched ON percentage bar.')
        
    def _bar_off(self):
        """if %Bar should be removed, figure out whether bar is already
        removed from screen."""
        switcher = {
            True: self._Bar.clear_bar,      #%Bar has to be removed
            False: self._print_second_line  #%Bar is already removed
        }
        # Get the function from switcher dictionary
        func = switcher[self._Bar.get_bar_state()]
        # Execute the function
        func()
        #print('Switched OFF percentage bar.')
        
    def _bar_update(self):
        """update the bar with the currently given percentage"""
        self._Bar.update(self._Kodi_state['percentage'] + self._percentage_offset)
        
    def _print_second_line(self):
        """more information on second line if %Bar is not present. This
        is a playground for later possibilites. Currently there is just
        the system time."""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self._VFD.vfd_print(current_time, alignment='c', line=1)
