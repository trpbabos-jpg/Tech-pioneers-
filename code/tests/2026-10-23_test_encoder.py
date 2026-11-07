# Stand 23.10.2026, alte Pinbelegung, siehe elektronik/pinbelegung.md "Frühere Stände".
# Fuer den aktuellen Aufbau die Pins anpassen (Motor 1: A GPIO13, B GPIO4; Motor 2: A GPIO25, B GPIO26).
# test_encoder.py
# Zaehlt die Impulse des Encoders von Motor 1 (FIT0520, 224 Impulse pro Radumdrehung).
# Verdrahtung damals:
#   blau    -> 3V3
#   schwarz -> GND
#   gelb    -> GPIO13 (Phase A)
#   gruen   -> GPIO14 (Phase B)
# Motor 2 damals: gelb GPIO19, gruen GPIO4.
# Rad von Hand drehen: vorwaerts zaehlt hoch, rueckwaerts runter.

from machine import Pin
import time

zaehler = 0


def zaehle(pin):
    global zaehler
    if enc_b.value():
        zaehler += 1
    else:
        zaehler -= 1


enc_a = Pin(13, Pin.IN, Pin.PULL_UP)
enc_b = Pin(14, Pin.IN, Pin.PULL_UP)
enc_a.irq(trigger=Pin.IRQ_RISING, handler=zaehle)

while True:
    print("Zaehler:", zaehler)
    time.sleep_ms(200)
