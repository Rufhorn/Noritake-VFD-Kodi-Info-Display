#!/usr/bin/python
# -*- coding: utf-8 -*-
import VFD_Interface as vfd
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Noritake_VFD_UI(vfd.Noritake_VFD):
    """Small display interface that fits to the noritake vfd display module
     CU20026SCPB-KS20AB. This class supports some basic alignment options
     for the character display.
     
     The class supports basic interaction with the display. The text can
     be aligned left ('l'), center ('c'), and right ('r') using the vfd_print
     function. Also vfd_print supports setting a frame of start- and stop-
     character the text is being aligned at (only l and r).
     
     The DisplayTracker function marks in an two-dimensional array (line x
     characters) already occupied positions of the display."""
     
    def __init__(self, rs, en, cs, d0, d1, d2, d3, d4, d5, d6, d7, cols=20, lines=2):
        """Setup the Display connections. Only 8 bit databus supported, for more
        details see description of class Noritake_VFD."""
        
        """call the setup function of class Noritake_VFD"""
        super().__init__(rs, en, cs, d0, d1, d2, d3, d4, d5, d6, d7, cols, lines)
        
        """Setup the DisplayTracker that indicates which characters are occupied 
        with signs and which are empty."""
        self._DisplayTracker = []
        self._setup_display_tracker()
        
        """clear the display and set the cursor invisible"""
        self._clear_display_tracker()
        self.cursor_invisible()
    
    def _setup_display_tracker(self):
        """The DisplayTracker is a two dimensional Array (lines x columns) that
        indicates which characters are currently occupied by signs.
        1 = occupied, 0 = empty"""
        
        for line in range(self._lines):
            line = []
            for column in range(self._cols):
                line.append(0)
            self._DisplayTracker.append(line)
            
    def _clear_display_tracker(self):
        """Clear the DisplayTracker and replaces all values with "0". 
        This Method should be called once the display is cleared. """
        for line in range(self._lines):
            for column in range(self._cols):
                self._DisplayTracker[line][column] = 0
            
                
    def get_display_tracker(self):
        """this function call returns the display tracker"""
        return self._DisplayTracker
    
    def vfd_clear_display(self):
        """clears the display and resets the DisplayTracker"""
        self.clear_display()
        self._clear_display_tracker()
        
    def vfd_clear_section(self, line=0, clear_start=1, length=1):
        """clear a given section with empty spaces"""
        
        """check, if the section is valid"""
        if clear_start == None or clear_start > self._cols or length < 1: return
        
        """calculate position and check if clearing exceeds the line length"""
        position = line*20 + clear_start
        if (position-1 + length) > (line+1)*20 : return
        
        """position the cursor and clear Display and display tracker"""
        self.set_cursor(position)
        for i in range(length):
            self.message(" ")
            self._DisplayTracker[line][i+clear_start-1] = 0
            
                        
    def vfd_print(self, TextMessage, alignment='l', line=0, frame_start=None, 
                  frame_stop=None, clear_display=False):
        """Print a given TextMessage to the Display.
            
        - Alignment: 'l' left, 'r' right, 'c' center
        - line defines the line number, start from '0'
        - frame_start is the number of the start-charater from left (>=1,<=20)
        - frame_stop is the number of the stop-character from left (>=1,<=20)
        - the alignment (l+r) is set within frame_start and frame_stop"""
        """check, if frame start and stop parameters are valid"""
        if frame_start == None or frame_start > self._cols or frame_start > frame_stop: frame_start = 1
        if frame_stop == None or frame_stop > self._cols or frame_start > frame_stop: frame_stop = self._cols
        
        """setup text print parameters"""
        TextStart = frame_start
        TextStop = frame_stop
        TextLength = len(TextMessage)
        
        """clear the whole display if necessary"""
        if clear_display: 
            self.vfd_clear_display()
        
        """calculate the text alignment in dependence of the given text window/frame
        by frame_start and frame_stop"""
        if TextLength < self._cols:
            if alignment == 'l': TextStart = frame_start
            elif alignment == 'r': TextStart = self._cols - TextLength - abs(frame_stop-self._cols) +1
            elif alignment == 'c': TextStart = (self._cols - TextLength)/2 +1
            else: 
                print("Alignment parameter not supportet! Please use 'l', 'r', 'c'!")
                return
        
        """calculate the stop of the text on screen in dependence of the given frame"""        
        TextStop = self._cols-(TextStart-1) -abs(self._cols-frame_stop)
        if TextLength <= TextStop: TextStop = TextLength
        
        """setup the correct line"""
        CursorStart = TextStart + (line*self._cols)
        self.set_cursor(CursorStart)
        
        """finally print the message"""
        self.message(TextMessage[:int(TextStop)])
        
        """update the DisplayTracker"""
        for value in range(int(TextStart),(int(TextStart)+int(TextStop))):
            self._DisplayTracker[line][value-1] = 1
 
