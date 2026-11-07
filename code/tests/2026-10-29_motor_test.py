# motor_test.py - beide Motoren testen und Drehrichtung einstellen
# Team Batman
#
# ANSCHLUSS (Steckplan Schritt 3 und 5):
#   GPIO32 -> MDD3A M2B, GPIO33 -> MDD3A M2A   (Motor 2, links)
#   GPIO27 -> MDD3A M1B, GPIO14 -> MDD3A M1A   (Motor 1, rechts)
#   MDD3A GND -> blaue Reihe (gemeinsame Masse!)
#   Motor 2 (links) an Klemme M2, Motor 1 (rechts) an Klemme M1
#   Akku rot -> Wippschalter -> VB+, Akku schwarz -> VB-
#
# SO TESTET IHR:
#   1. Roboter hochheben oder aufbocken, die Raeder muessen frei drehen.
#   2. USB anstecken, Programm starten, DANN Wippschalter an.
#   3. Bei Test 1 darf sich nur das LINKE Rad drehen, und zwar VORWAERTS.
#      Dreht es rueckwaerts: RICHTUNG_LINKS = -1 setzen.
#      Dreht sich das rechte Rad: Kabel an den Pins vertauscht, Steckplan pruefen.
#   4. Bei Test 2 genauso fuer das RECHTE Rad und RICHTUNG_RECHTS.
#   5. Die beiden Werte RICHTUNG_LINKS und RICHTUNG_RECHTS auch in main.py eintragen.

from machine import Pin, PWM
import time

# ---------- Pins (aus unserem Steckplan) ----------
M2B, M2A = 32, 33   # Motor 2, links
M1B, M1A = 27, 14   # Motor 1, rechts

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
TEST_GESCHW = 40       # Geschwindigkeit fuer die Tests in %


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
    # Motor 2 = links (Kopie von motor1, Lab-Aufgabe Kap. 4b)
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
    print("  Motor links:", links, "%   Motor rechts:", rechts, "%")


def rampe(von, bis, schritt):
    # wie rampe() aus Kap. 4b, nur fuer beide Motoren
    g = von
    while g != bis:
        motoren(g, g)
        time.sleep_ms(300)
        g = g + schritt
    motoren(bis, bis)


try:
    print("Motor-Test startet in 3 Sekunden - Raeder frei?")
    time.sleep(3)

    print("Test 1: nur LINKS vorwaerts")
    motoren(TEST_GESCHW, 0)
    time.sleep(2)
    motoren(0, 0)
    time.sleep(1)

    print("Test 2: nur RECHTS vorwaerts")
    motoren(0, TEST_GESCHW)
    time.sleep(2)
    motoren(0, 0)
    time.sleep(1)

    print("Test 3: beide vorwaerts, sanft hoch und runter")
    rampe(0, 60, 10)
    time.sleep(1)
    rampe(60, 0, -10)
    time.sleep(1)

    print("Test 4: beide rueckwaerts")
    rampe(0, -40, -10)
    time.sleep(1)
    rampe(-40, 0, 10)
    time.sleep(1)

    print("Test 5: Rechtskurve (links schneller)")
    motoren(50, 25)
    time.sleep(2)
    motoren(0, 0)
    time.sleep(1)

    print("Test 6: auf der Stelle drehen (links vor, rechts zurueck)")
    motoren(40, -40)
    time.sleep(2)
    motoren(0, 0)

    print("Alle Tests fertig")
finally:
    motoren(0, 0)
    print("Programm beendet, Motoren aus")
