# boot.py - laeuft auf dem ESP32 VOR main.py
# Team Batman, 17.11.2026
# GPIO14 (Motor rechts, M1A) gibt beim Hochfahren ein PWM-Signal aus,
# dadurch dreht das rechte Rad nach dem Einschalten kurz. Hier werden alle
# Motorpins so frueh wie moeglich auf 0 gesetzt.
from machine import Pin

for nummer in (14, 27, 33, 32):
    Pin(nummer, Pin.OUT, value=0)
