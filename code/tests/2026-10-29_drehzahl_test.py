# drehzahl_test.py - Drehzahl beider Motoren ueber die Encoder messen
# Team Batman
#
# ANSCHLUSS (Steckplan Schritt 2 und 4):
#   Encoder Motor 2 (links):  gelb -> GPIO25, gruen -> GPIO26, blau -> 3V3, schwarz -> GND
#   Encoder Motor 1 (rechts): gelb -> GPIO13, gruen -> GPIO4,  blau -> 3V3, schwarz -> GND
#   Encoder NIE an die rote Reihe (5 V)!
#   Motoren wie in motor_test.py
#
# SO TESTET IHR:
#   1. Vorher motor_test.py: RICHTUNG_LINKS und RICHTUNG_RECHTS muessen stimmen.
#   2. Roboter hochheben, Raeder frei. USB an, Programm starten, Wippschalter an.
#   3. Bei 25, 50, 75 und 100 % wird je 1 s lang gezaehlt.
#   4. Bei 100 % sollten es ca. 240 U/min sein (letzte Woche: 244 und 247).
#   5. Impulse = 0 bei einem Motor: Encoder-Kabel pruefen (gelb, blau an 3V3).
#   6. Den Unterschied links/rechts notieren, den brauchen wir fuer KP in main.py.

from machine import Pin, PWM
import time

# ---------- Pins (aus unserem Steckplan) ----------
M2B, M2A = 32, 33         # Motor 2, links
M1B, M1A = 27, 14         # Motor 1, rechts
ENC2_A, ENC2_B = 25, 26   # Encoder Motor 2, links
ENC1_A, ENC1_B = 13, 4    # Encoder Motor 1, rechts

# Motoren als Allererstes auf 0
m1a = PWM(Pin(M1A), freq=20000, duty_u16=0)
m1b = PWM(Pin(M1B), freq=20000, duty_u16=0)
m2a = PWM(Pin(M2A), freq=20000, duty_u16=0)
m2b = PWM(Pin(M2B), freq=20000, duty_u16=0)

# ---------- Einstellungen ----------
RICHTUNG_LINKS = 1       # Testtaste M2A am MDD3A dreht links vorwaerts
RICHTUNG_RECHTS = -1     # Motor rechts ist gespiegelt eingebaut (Kabel: M1A an 14, M1B an 27)
ANLAUF_LINKS = 20         # 29.10. kalibrieren.py in der Luft: links dreht ab 20 %
ANLAUF_RECHTS = 20        # 29.10.: gemessen 16 %, aber gleicher Wert wie links laeuft gleichmaessiger (drehzahl_test.py)
FAKTOR_LINKS = 0.94       # 29.10. drehzahl_test.py in der Luft: links ca. 4-5 % schneller
IMPULSE_PRO_UMDREHUNG = 224   # laut Folie 23, Kap. 4b
RAD_DURCHMESSER = 8.0         # in cm
MESSZEIT_MS = 1000            # 1 Sekunde zaehlen
STUFEN = [15, 25, 50, 75, 100]    # diese Geschwindigkeiten werden getestet


def begrenzen(x, unten, oben):
    # aus Kap. 4d
    return max(unten, min(oben, x))


def motor1(geschwindigkeit):
    # Motor 1 = rechts (wie motor() aus Kap. 4b)
    geschwindigkeit = begrenzen(geschwindigkeit, -100, 100)
    # Anlauf ausgleichen (gemessen mit kalibrieren.py):
    # schon 1 % soll das Rad gerade so drehen, 100 % bleibt 100 %
    if geschwindigkeit > 0:
        geschwindigkeit = ANLAUF_RECHTS + geschwindigkeit * (100 - ANLAUF_RECHTS) / 100
    elif geschwindigkeit < 0:
        geschwindigkeit = -ANLAUF_RECHTS + geschwindigkeit * (100 - ANLAUF_RECHTS) / 100
    geschwindigkeit = geschwindigkeit * RICHTUNG_RECHTS
    duty = int(abs(geschwindigkeit) * 65535 / 100)
    if geschwindigkeit > 0:
        m1a.duty_u16(duty)
        m1b.duty_u16(0)
    elif geschwindigkeit < 0:
        m1a.duty_u16(0)
        m1b.duty_u16(duty)
    else:
        m1a.duty_u16(0)
        m1b.duty_u16(0)


def motor2(geschwindigkeit):
    # Motor 2 = links
    geschwindigkeit = begrenzen(geschwindigkeit, -100, 100)
    # links ist schneller als rechts (drehzahl_test.py), deshalb etwas weniger Gas
    geschwindigkeit = geschwindigkeit * FAKTOR_LINKS
    # Anlauf ausgleichen (gemessen mit kalibrieren.py):
    # schon 1 % soll das Rad gerade so drehen, 100 % bleibt 100 %
    if geschwindigkeit > 0:
        geschwindigkeit = ANLAUF_LINKS + geschwindigkeit * (100 - ANLAUF_LINKS) / 100
    elif geschwindigkeit < 0:
        geschwindigkeit = -ANLAUF_LINKS + geschwindigkeit * (100 - ANLAUF_LINKS) / 100
    geschwindigkeit = geschwindigkeit * RICHTUNG_LINKS
    duty = int(abs(geschwindigkeit) * 65535 / 100)
    if geschwindigkeit > 0:
        m2a.duty_u16(duty)
        m2b.duty_u16(0)
    elif geschwindigkeit < 0:
        m2a.duty_u16(0)
        m2b.duty_u16(duty)
    else:
        m2a.duty_u16(0)
        m2b.duty_u16(0)


def motoren(links, rechts):
    motor2(links)
    motor1(rechts)


# ---------- Encoder: Impulse zaehlen mit Interrupt (Fortgeschrittene Kap. 4c) ----------
enc_links = Pin(ENC2_A, Pin.IN, Pin.PULL_UP)
enc_rechts = Pin(ENC1_A, Pin.IN, Pin.PULL_UP)
impulse_links = 0
impulse_rechts = 0


def zaehle_links(pin):
    global impulse_links
    impulse_links = impulse_links + 1


def zaehle_rechts(pin):
    global impulse_rechts
    impulse_rechts = impulse_rechts + 1


enc_links.irq(trigger=Pin.IRQ_RISING, handler=zaehle_links)
enc_rechts.irq(trigger=Pin.IRQ_RISING, handler=zaehle_rechts)


def auswerten(name, impulse):
    # Impulse -> Umdrehungen -> U/s -> U/min -> cm/s
    umdrehungen = impulse / IMPULSE_PRO_UMDREHUNG
    ups = umdrehungen / (MESSZEIT_MS / 1000)
    upm = ups * 60
    umfang = 3.1416 * RAD_DURCHMESSER
    cms = ups * umfang
    print("  ", name, impulse, "Impulse ->", round(ups, 2), "U/s ->",
          round(upm), "U/min ->", round(cms, 1), "cm/s")
    return upm


try:
    print("Drehzahl-Test startet in 3 Sekunden - Raeder frei?")
    time.sleep(3)

    for prozent in STUFEN:
        print()
        print("Motoren auf", prozent, "%")
        motoren(prozent, prozent)
        time.sleep(1)      # warten, bis die Drehzahl gleichmaessig ist

        # Zaehler auf 0 und genau MESSZEIT_MS lang zaehlen
        impulse_links = 0
        impulse_rechts = 0
        time.sleep_ms(MESSZEIT_MS)
        l = impulse_links
        r = impulse_rechts

        upm_l = auswerten("links: ", l)
        upm_r = auswerten("rechts:", r)

        if upm_r > 0:
            unterschied = (upm_l - upm_r) / upm_r * 100
            print("   Unterschied links zu rechts:", round(unterschied, 1), "%")

    print()
    print("Test fertig")
finally:
    motoren(0, 0)
    print("Programm beendet, Motoren aus")
