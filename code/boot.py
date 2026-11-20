# Motorpins beim Start aus
from machine import Pin

Pin(33, Pin.OUT, value=0)       # Motor rechts
Pin(32, Pin.OUT, value=0)
Pin(26, Pin.OUT, value=0)       # Motor links
Pin(25, Pin.OUT, value=0)
