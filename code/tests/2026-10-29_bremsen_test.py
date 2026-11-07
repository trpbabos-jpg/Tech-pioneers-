# bremsen_test.py - auf eine Wand zufahren und sanft davor stehen bleiben
# Team Batman
#
# Hier testen wir nur Anfahren und Bremsen mit dem Ultraschall,
# OHNE die Wand zu beruehren und ohne Encoder-Korrektur.
# Damit finden wir gute Werte fuer BREMSEN_AB, SCHRITT_HOCH und SCHRITT_RUNTER.
#
# ANSCHLUSS: Motoren wie in motor_test.py, Ultraschall wie in ultraschall_test.py
#
# SO TESTET IHR:
#   1. Roboter ca. 150 cm vor eine Wand oder einen grossen Karton stellen.
#   2. USB an, Programm starten, Wippschalter an. Nach 3 s faehrt er los.
#   3. Er soll sanft anfahren, ab BREMSEN_AB langsam werden und bei
#      ca. STOPP_BEI stehen bleiben.
#   4. Am Ende steht in der Shell, bei wie viel cm er wirklich steht.
#   5. Erst ohne Ball, dann mit Ball testen. Faellt der Ball raus:
#      SCHRITT_HOCH und SCHRITT_RUNTER kleiner machen.

from machine import Pin, PWM, time_pulse_us
import time

# ---------- Pins (aus unserem Steckplan) ----------
M2B, M2A = 32, 33   # Motor 2, links
M1B, M1A = 27, 14   # Motor 1, rechts
TRIG = 19
ECHO = 35

# Motoren als Allererstes auf 0
m1a = PWM(Pin(M1A), freq=20000, duty_u16=0)
m1b = PWM(Pin(M1B), freq=20000, duty_u16=0)
m2a = PWM(Pin(M2A), freq=20000, duty_u16=0)
m2b = PWM(Pin(M2B), freq=20000, duty_u16=0)

# ---------- Einstellungen ----------
RICHTUNG_LINKS = 1       # Testtaste M2A am MDD3A dreht links vorwaerts
RICHTUNG_RECHTS = -1     # Motor rechts ist gespiegelt eingebaut (Kabel: M1A an 14, M1B an 27)

ZYKLUS_MS = 50         # fester Takt (Kap. 4d)
ANLAUF_LINKS = 20         # 29.10. kalibrieren.py in der Luft: links dreht ab 20 %
ANLAUF_RECHTS = 20        # 29.10.: gemessen 16 %, aber gleicher Wert wie links laeuft gleichmaessiger (drehzahl_test.py)
FAKTOR_LINKS = 0.94       # 29.10. drehzahl_test.py in der Luft: links ca. 4-5 % schneller
START = 5              # damit faengt er an
VMAX = 50              # in %
KRIECHEN = 15          # Kriechtempo in % (nach neuer Kalibrierung anpassen)
SCHRITT_HOCH = 2       # % pro Takt schneller
SCHRITT_RUNTER = 3     # % pro Takt langsamer
BREMSEN_AB = 60        # ab hier (cm) wird langsamer
STOPP_BEI = 15         # hier (cm) bleibt er stehen


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


# ---------- Ultraschall (Kap. 4a) ----------
trig = Pin(TRIG, Pin.OUT)
echo = Pin(ECHO, Pin.IN)
trig.value(0)


def messen():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400   # kein Echo
    return laufzeit * 0.0343 / 2


class Median:
    # Lab-Aufgabe Kap. 4d

    def __init__(self, n):
        self.n = n
        self.werte = []

    def neu(self, wert):
        self.werte.append(wert)
        if len(self.werte) > self.n:
            self.werte.pop(0)
        sortiert = sorted(self.werte)
        return sortiert[len(sortiert) // 2]


median = Median(3)
g = 0
bremsen = False    # einmal am Bremsen, wird er nicht mehr schneller

try:
    print("Bremsen-Test: Start in 3 Sekunden - Platz machen!")
    time.sleep(3)

    g = START
    fahren = True
    takt = time.ticks_ms()

    while fahren:
        takt = time.ticks_add(takt, ZYKLUS_MS)

        d = median.neu(messen())

        if d < BREMSEN_AB:
            bremsen = True

        if d < STOPP_BEI:
            # am Ziel: stehen bleiben
            g = 0
            fahren = False
        elif bremsen:
            # sanft langsamer bis Kriechtempo
            if g > KRIECHEN:
                g = g - SCHRITT_RUNTER
                if g < KRIECHEN:
                    g = KRIECHEN
        else:
            # sanft schneller bis VMAX
            if g < VMAX:
                g = g + SCHRITT_HOCH
                if g > VMAX:
                    g = VMAX

        motoren(g, g)
        print("Abstand:", round(d, 1), "cm  Geschwindigkeit:", g, "%  bremsen:", bremsen)

        rest = time.ticks_diff(takt, time.ticks_ms())
        time.sleep_ms(max(0, rest))

    motoren(0, 0)
    time.sleep(1)     # ausrollen lassen

    # wo steht er wirklich? 5 Messungen, davon der Median
    werte = []
    for i in range(5):
        werte.append(messen())
        time.sleep_ms(60)
    werte.sort()
    print()
    print("Er steht bei", round(werte[2], 1), "cm (Ziel war", STOPP_BEI, "cm)")
finally:
    motoren(0, 0)
    print("Programm beendet, Motoren aus")
