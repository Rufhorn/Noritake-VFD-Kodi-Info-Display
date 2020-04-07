#!/usr/bin/python
# -*- coding: utf-8 -*-
import VFD_UI
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class VfdPercentageBar(object):
    """Creates an Percentage Bar Object that can be printed on a Noritake
    VFD Textdisplay Model CU20026SCPB-KS20AB. Once the bar is setup it can
    be update by update(%). Also the Bar can be removed and printed
    again as long as the object exists."""
    
    def __init__(self, vfd:VFD_UI.Noritake_VFD_UI, line=1, bar_start=None, bar_stop=None, bar_sign=None):
        """Input is a Noritake_VFD_UI object. Also you can choose placement
        and length of the bar by set line number and number of start and stop
        of the bar."""
        
        """initialize all necessary parameters"""
        self._vfd = vfd
        self._bar_start = bar_start
        self._bar_stop = bar_stop
        #self._bar_tracker = []
        #self._current_position = 0
        self._bar_sign = bar_sign
        
        """get number of lines and colums from the display"""
        self._cols = self._vfd.get_cols()
        self._lines = self._vfd.get_lines()
        self._line = line
        
        """setup default parameters if none are given. Default is line 2 using
        the full width of the display."""
        if self._line > self._lines: self._line = self._lines-1
        if self._bar_start == None: self._bar_start = 1
        if self._bar_stop == None: self._bar_stop = self._cols
        if self._bar_sign == None: self._bar_sign = '.'
        
        """set flag if a new bar needs to be set up"""
        self._flag_new_setup_needed = True
        self._flag_bar_cleared = True
        
        #self.setup_bar()  
        
    def setup_bar(self):
        """prints brackets on screen to define the bar area."""
        
        """check if bar is already existing"""
        if self._flag_bar_cleared == False:
            print("Please execute clear_bar() first to remove previous bar!")
            return
        
        """calculate the offset for start- and stop-command"""
        self._offset = self._line*self._cols
        bar_start = self._bar_start + self._offset
        bar_stop = self._bar_stop + self._offset
        
        """clear the desired section on screen"""
        self._vfd.vfd_clear_section(line=self._line, clear_start=self._bar_start, length=(self._bar_stop-self._bar_start+1))
        
        """print the brackets"""
        self._vfd.set_cursor(bar_start)
        self._vfd.message('[')
        self._vfd.set_cursor(bar_stop)
        self._vfd.message(']')
        self._bar_length = bar_stop - bar_start -1
        
        """set flag, that a bar was set up on screen"""
        self._flag_new_setup_needed = False
        self._flag_bar_cleared = False
    
    def clear_bar(self):
        """remove the bar from screen"""
        
        """clear section"""
        self._vfd.vfd_clear_section(line=self._line, clear_start=self._bar_start, length=(self._bar_stop-self._bar_start+1))
        
        """set tracking flag"""
        self._flag_bar_cleared = True
        self._flag_new_setup_needed = True
        
    def update(self, percentage):
        """update the percentage print on screen"""
        
        """check if basic settings of bar have changed"""
        if self._flag_new_setup_needed:
            print("Please execute setup_bar() first to create a new bar!")
            return
        
        """check percentage range"""
        if int(percentage) > 100: percentage = 100
        if int(percentage) < 0: percentage = 0
        
        """calculate the length of the bar to be printed and setup string to print"""
        temp = int(self._bar_length * (percentage/100))
        bar_string = ''
        
        """fill string with bar signs and fill up with space until end of bar"""
        for i in range(temp): bar_string += self._bar_sign
        for i in range(self._bar_length - temp): bar_string += ' '
        
        """print bar to screen"""
        self._vfd.vfd_print(bar_string, line=self._line, frame_start=(self._bar_start+1), frame_stop=(self._bar_stop-1))
        
    def set_bar_start(self, new_start):
        """set a new start position for the bar"""
        if self._flag_bar_cleared:
            self._bar_start = new_start
            self._flag_new_setup_needed = True
        else:
            print("Remove old bar first!")
        
    def set_bar_stop(self, new_stop):
        """set a new stop position for the bar"""
        if self._flag_bar_cleared:
            self._bar_stop = new_stop
            self._flag_new_setup_needed = True
        else:
            print("Remove old bar first!")
            
    def set_bar_sign(self, new_sign):
        """change the sign that is used to fill the bar. By default these
        are dots."""
        self._bar_sign = new_sign
        
    def set_bar_line(self, new_line):
        """change the line the bar is printed on."""
        if self._flag_bar_cleared:
            self._line = new_line
            self._flag_new_setup_needed = True
        else:
            print("Remove old bar first!")
            
    def get_bar_state(self):
        """returns true if the bar exists, false if not."""
        return not self._flag_bar_cleared



