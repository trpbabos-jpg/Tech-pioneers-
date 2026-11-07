# Stand 20.10.2026 (erster Aufbau), alte Pinbelegung, siehe elektronik/pinbelegung.md "Frühere Stände".
# Fuer den aktuellen Aufbau die Pins oben im Programm anpassen.
# ultraschall_test.py
# Abstandswächter: ESP32 + Ultraschallsensor HC-SR04 + LED
# Verdrahtung (wie in den Folien, Kap. 4a):
#   VCC  -> 5V
#   Gnd  -> GND
#   Trig -> GPIO26
#   Echo -> Spannungsteiler (1 kOhm / 2 kOhm) -> GPIO25
#           ACHTUNG: Echo liefert 5 V, der ESP32 verträgt nur 3,3 V!
#   LED mit 220 Ohm Vorwiderstand -> GPIO2

from machine import Pin, time_pulse_us
import time

trig = Pin(26, Pin.OUT)   # Trigger
echo = Pin(25, Pin.IN)    # Echo
led = Pin(2, Pin.OUT)     # LED
trig.value(0)
led.value(0)

N = 5            # Anzahl Messungen für den Mittelwert
SCHWELLE = 30    # Schwellwert in cm


def messen():
    # 10 us langer Startpuls
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    # Dauer des Echo-Pulses messen (höchstens 30000 us warten)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400   # kein Echo: nichts in Reichweite
    return laufzeit * 0.0343 / 2


try:
    while True:
        summe = 0
        i = 0
        while i < N:
            wert = messen()
            summe = summe + wert
            i = i + 1
            print("Messung", i, ":", round(wert, 1),
                  "cm  Summe:", round(summe, 1))
            time.sleep_ms(60)   # altes Echo abklingen lassen

        mittelwert = summe / N
        print("Mittelwert:", round(mittelwert, 1), "cm")

        if mittelwert < SCHWELLE:
            led.value(1)
            print("Entscheidung:", round(mittelwert, 1),
                  "<", SCHWELLE, "-> LED an")
        else:
            led.value(0)
            print("Entscheidung:", round(mittelwert, 1),
                  ">=", SCHWELLE, "-> LED aus")
        print()
        time.sleep(1)
finally:
    led.value(0)
    print("Programm beendet, LED aus")
