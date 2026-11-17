# taster_test.py - Stossschalter testen und TASTER_GEDRUECKT bestimmen
# Team Batman
#
# ANSCHLUSS (Steckplan Schritt 7):
#   Kontakt 1 -> GPIO22 (obere Reihe)
#   Kontakt 2 -> blaue Reihe (GND)
#   Kein Widerstand noetig, der Pull-up ist im ESP32 (Kap. 4c)
#
# SO TESTET IHR:
#   1. Programm starten. Alle 0,2 s steht in der Shell "roh: 0" oder "roh: 1".
#   2. Nicht druecken und ablesen. Dann gedrueckt halten und ablesen.
#   3. Den Wert beim GEDRUECKTEN Taster als TASTER_GEDRUECKT eintragen
#      (hier und in main.py). Laut Kap. 4c ist es beim Oeffner eine 1.
#   4. Danach 10x druecken: Es muessen genau 10 Druecke gezaehlt werden.
#      Kommen mehr: ENTPRELLZEIT erhoehen (z. B. 50).
#   5. Kabel absichtlich abziehen: Beim Oeffner zeigt "roh" dann "gedrueckt".
#
# Ergebnis 17.11.2026: funktioniert, TASTER_GEDRUECKT = 1

from machine import Pin
import time

TASTER = 22

TASTER_GEDRUECKT = 1    # nach Schritt 3 eintragen
ENTPRELLZEIT = 30       # ms (Kap. 4c)

taster = Pin(TASTER, Pin.IN, Pin.PULL_UP)

vorher = taster.value()


def istTasteGedrueckt():
    # wie in Kap. 4c, nur mit TASTER_GEDRUECKT statt fest 1
    global vorher
    jetzt = taster.value()
    if jetzt == vorher:
        return False     # kein Wechsel
    # Prellen abwarten
    time.sleep_ms(ENTPRELLZEIT)
    vorher = jetzt
    # True nur beim Druecken
    return jetzt == TASTER_GEDRUECKT


druecke = 0
zaehler = 0
print("Bereit: Taster druecken!")

while True:
    if istTasteGedrueckt():
        druecke = druecke + 1
        print("Druck erkannt, Nummer", druecke)

    # alle 20 x 10 ms = 0,2 s den Rohwert anzeigen
    zaehler = zaehler + 1
    if zaehler >= 20:
        roh = taster.value()
        if roh == TASTER_GEDRUECKT:
            print("roh:", roh, "-> gedrueckt")
        else:
            print("roh:", roh, "-> nicht gedrueckt")
        zaehler = 0

    time.sleep_ms(10)
