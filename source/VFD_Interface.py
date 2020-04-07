#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

#set pin numbering as on the board
GPIO.setmode(GPIO.BCM)

class Noritake_VFD(object):
    """Class to represent and interact with Noritake CU20026SCPB-KS20AB module."""

    def __init__(self, rs, en, cs, d0, d1, d2, d3, d4, d5, d6, d7, cols=20, lines=2):
        """Initialize the VFD. The Model CU20026SCPB-KS20AB from Noritake only
        supports the 8 bit data bus (d0-d7). The Register select equivalent (rs) is
        named "A0" and the Enable (en) equivalent is named "RD". The Display 
        supports a read mode, but for safety reasons (the display IO run on 5V) the 
        Read/Write (wr) pin is connected to GND (write only)."""        
            
        """Save column and line state."""
        self._cols = cols
        self._lines = lines
        
        """Save GPIO state and pin numbers."""
        self._rs = rs   #A0 is the equiv to "register select" for HD44780
        self._en = en   #RD is the equiv to "enable"
        self._cs = cs   #Chip select LOW=selected, HIGH=deselected
        self._d0 = d0   #\
        self._d1 = d1   # |
        self._d2 = d2   # |
        self._d3 = d3   # | -- 8 Bit Data Bus
        self._d4 = d4   # | 
        self._d5 = d5   # |
        self._d6 = d6   # |
        self._d7 = d7   #/
        
        """Setup all pins as outputs and LOW."""
        for pin in (rs, en, cs, d0, d1, d2, d3, d4, d5, d6, d7):
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) 
            
        """Clear display and set to home position."""
        self.clear_display()
        
        """Map german characters to their commands"""
        self._german_characters = {'Ä':0x5B,'Ö':0x5C,']':0x5D,'Ü':0x5E,
                                   'ä':0x7B,'ö':0x7C,'ü':0x7D,'ß':0x7E,}
                             
    def write8(self, value, char_mode=False):
        """Write 8-bit value in character or data mode.  Value should be an int
        value from 0-255, and char_mode is True if character data or False if
        non-character data (default).
        """
        # One millisecond delay to prevent writing too quickly.
        self._delay_microseconds(1000)
        # Set character / data bit.
        GPIO.output(self._rs, char_mode)
        # Write 8 bits.
        GPIO.output(self._d0, value & 0x01)
        GPIO.output(self._d1, value & 0x02)
        GPIO.output(self._d2, value & 0x04)
        GPIO.output(self._d3, value & 0x08)
        GPIO.output(self._d4, value & 0x10)
        GPIO.output(self._d5, value & 0x20)
        GPIO.output(self._d6, value & 0x40)
        GPIO.output(self._d7, value & 0x80)
        #toggle the pulse to write the data
        self._pulse_enable()

    def _delay_microseconds(self, microseconds):
        """ Busy wait in loop because delays are generally very short (few microseconds)."""
        end = time.time() + (microseconds/1000000.0)
        while time.time() < end:
            pass
            
    def _pulse_enable(self):
        """Pulse the clock enable line off, on, off to send command."""
        GPIO.output(self._en, False)
        self._delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 200ns
        GPIO.output(self._en, True)
        self._delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 200ns
        GPIO.output(self._en, False)
        self._delay_microseconds(1)       # commands need > 37us to settle

    def message(self, text):
        """Write text to display"""
        # Iterate through each character.
        for char in text:
            if char in self._german_characters:
                self._german_font()
                self.write8(self._german_characters[char], False)
                self._english_font()
            else: self.write8(ord(char), False)
            
    def set_cursor(self, position):
        """Set the cursor to a given position, that has to be given as integer."""
        #check, if the given position is within the space of the display
        if position >= 1 or position <= (self._cols * self._lines):
            self.write8(int(position-1), True)
        else:
            print("Index out of Range!") 
            return
        
    def select(self):
        """For selection pull Chip-Select-Pint LOW."""
        GPIO.output(self._cs, GPIO.LOW)
    
    def deselect(self):
        """For deselection pull Chip-Select-Pint HIGH."""
        GPIO.output(self._cs, GPIO.HIGH)
        
    def home(self):
        """Sets cursor to home position."""
        self.write8(0x0B)
        
    def back_space(self):
        """Move cursor one position to the left."""
        self.write8(0x08)
        
    def horizontal_tab(self):
        """Move cursor one position to the right."""
        self.write8(0x09)
        
    def line_feed(self):
        """Cursor moves down. If cursor was in line 2 before, the upper
        line is cleared (cursor moves "further" down)"""
        self.write8(0x0A)
        
    def clear_display(self):
        """Clear display and set cursor to home position."""
        self.write8(0x0C)
        
    def carriage_return(self):
        """carriage return."""
        self.write8(0x0D)
           
    def cursor_underline(self):
        """Underlines the cursor."""
        self.write8(0x13)
    
    def cursor_blinking(self):
        """Sets the cursor blinking."""
        self.write8(0x14)
        
    def cursor_invisible(self):
        """Sets the cursor invisible."""
        self.write8(0x15)
        
    def cursor_blinking_underline(self):
        """Sets the cursor underlined and blinking."""
        self.write8(0x16)
        
    def _english_font(self):
        """Extra font for extra characters: english"""
        self.write8(0x1A)
        
    def _danish_font(self):
        """Extra font for extra characters: danish"""
        self.write8(0x1C)
        
    def _general_european_font(self):
        """Extra font for extra characters: general european"""
        self.write8(0x1D)
        
    def _swedish_font(self):
        """Extra font for extra characters: swedish"""
        self.write8(0x1E)
        
    def _german_font(self):
        """Extra font for extra characters: german"""
        self.write8(0x1F)
        
    def software_reset(self):
        """sofware reset of the VFD display"""
        self.write8(0x51, True)
        
    def get_cols(self):
        """returns number of columns of the vfd"""
        return self._cols
        
    def get_lines(self):
        """returns number of lines of the vfd"""
        return self._lines
