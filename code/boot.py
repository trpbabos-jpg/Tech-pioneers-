# boot.py - laeuft auf dem ESP32 VOR main.py
# Team Batman, 17.11.2026
# M1A lag frueher an GPIO14, der beim Hochfahren ein PWM-Signal ausgibt,
# deshalb am 17.11. auf GPIO21 umgesteckt. Zur Sicherheit werden hier alle
# Motorpins so frueh wie moeglich auf 0 gesetzt.
from machine import Pin

for nummer in (21, 27, 33, 32):
    Pin(nummer, Pin.OUT, value=0)
