# main.py - Wall-Sprint: hin, sanft an die Wand, rueckwaerts zurueck
# Team Batman

from machine import Pin, PWM, time_pulse_us
import time

# ----- Pins (Steckplan) -----
m1a = PWM(Pin(14), freq=20000, duty_u16=0)   # Motor rechts
m1b = PWM(Pin(27), freq=20000, duty_u16=0)
m2a = PWM(Pin(33), freq=20000, duty_u16=0)   # Motor links
m2b = PWM(Pin(32), freq=20000, duty_u16=0)
trig = Pin(19, Pin.OUT)
echo = Pin(35, Pin.IN)
taster = Pin(22, Pin.IN, Pin.PULL_UP)
enc_links = Pin(25, Pin.IN, Pin.PULL_UP)
enc_rechts = Pin(13, Pin.IN, Pin.PULL_UP)

# ----- Gemessen mit kalibrieren.py und drehzahl_test.py -----
ANLAUF = 20                 # unter 20 % dreht kein Rad
FAKTOR_LINKS = 0.7          # motorkraft links beim Vorwaertsfahren
FAKTOR_LINKS_ZURUECK = 0.7  # motorkraft links beim Rueckwaertsfahren (ausprobieren)

# ----- Fahren (ausprobieren) -----
VMAX = 80             # Hoechstgeschwindigkeit in %
KRIECHEN = 20         # Tempo kurz vor der Wand in %
SCHRITT_HOCH = 6      # % schneller pro Takt
SCHRITT_RUNTER = 7    # % langsamer pro Takt
BREMSEN_AB = 50       # ab diesem Abstand in cm bremsen
BREMSEN_AB_ZURUECK = 45   # rueckwaerts: ab dieser Reststrecke in cm bremsen
TAKT_MS = 50
KP = 0.5              # Encoder-Korrektur fuer die Geradeausfahrt
CM_PRO_IMPULS = 3.1416 * 8.0 / 224   # Radumfang / Impulse pro Umdrehung


# ----- Motoren (Kap. 4b) -----
def motor(pin_a, pin_b, geschwindigkeit):
    # Anlauf ausgleichen: 1 % dreht schon, 100 % bleibt 100 %
    if geschwindigkeit > 0:
        geschwindigkeit = ANLAUF + geschwindigkeit * (100 - ANLAUF) / 100
    elif geschwindigkeit < 0:
        geschwindigkeit = -ANLAUF + geschwindigkeit * (100 - ANLAUF) / 100
    duty = int(min(abs(geschwindigkeit), 100) * 65535 / 100)
    if geschwindigkeit > 0:
        pin_a.duty_u16(duty)
        pin_b.duty_u16(0)
    elif geschwindigkeit < 0:
        pin_a.duty_u16(0)
        pin_b.duty_u16(duty)
    else:
        pin_a.duty_u16(0)
        pin_b.duty_u16(0)


def motoren(links, rechts):
    # vorwaerts und rueckwaerts kann links unterschiedlich stark sein
    if links >= 0:
        motor(m2a, m2b, links * FAKTOR_LINKS)
    else:
        motor(m2a, m2b, links * FAKTOR_LINKS_ZURUECK)
    motor(m1a, m1b, -rechts)      # rechter Motor ist gespiegelt eingebaut


# ----- Ultraschall (Kap. 4a) -----
def messen():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400
    return laufzeit * 0.0343 / 2


class Median:
    # merkt sich die letzten 3 Messungen und gibt die mittlere zurueck,
    # damit eine einzelne Fehlmessung nicht stoert (Lab-Aufgabe Kap. 4d)

    def __init__(self):
        self.werte = []

    def neu(self, wert):
        self.werte.append(wert)
        if len(self.werte) > 3:
            self.werte.pop(0)
        sortiert = sorted(self.werte)
        return sortiert[len(sortiert) // 2]


median = Median()


# ----- Taster (Kap. 4c) -----
def wand_beruehrt():
    # 7-mal nachschauen, damit kurzes Zucken beim Fahren nicht ausloest
    for i in range(7):
        if taster.value() != 1:
            return False
        time.sleep_ms(2)
    return True


# ----- Encoder (Fortgeschrittene Kap. 4b/4c) -----
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


def gefahren_cm():
    return (impulse_links + impulse_rechts) / 2 * CM_PRO_IMPULS


def geradeaus(g, richtung):
    # Rad mit mehr Impulsen ist weiter gefahren -> etwas langsamer
    korrektur = KP * (impulse_links - impulse_rechts)
    # je langsamer, desto schwaecher die Korrektur
    # (bei 80 % hoechstens 8 %, bei 20 % hoechstens 2 %)
    grenze = 8 * g / VMAX
    korrektur = max(-grenze, min(grenze, korrektur))
    motoren((g - korrektur) * richtung, (g + korrektur) * richtung)


# ----- Ablauf -----
try:
    motoren(0, 0)
    time.sleep(3)                     # Regel: 2 bis 10 s an der Startwand

    # 1. Hinfahren: sanft schneller bis VMAX, bis die Wand nah ist
    print("Hinfahren")
    g = 0
    while median.neu(messen()) > BREMSEN_AB and not wand_beruehrt():
        g = min(g + SCHRITT_HOCH, VMAX)
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
    print("diff hin:", impulse_links - impulse_rechts)

    # 2. Sanft bremsen auf Kriechtempo, bis der Taster die Wand beruehrt
    print("Bremsen")
    while not wand_beruehrt():
        g = max(g - SCHRITT_RUNTER, KRIECHEN)
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
    motoren(0, 0)
    strecke = gefahren_cm()
    print("Wand beruehrt nach", round(strecke), "cm")
    time.sleep_ms(500)

    # 3. Rueckwaerts dieselbe Strecke zurueck, am Ende wieder sanft
    print("Zurueck")
    impulse_links = 0
    impulse_rechts = 0
    g = 0
    while gefahren_cm() < strecke:
        if strecke - gefahren_cm() > BREMSEN_AB_ZURUECK:
            g = min(g + SCHRITT_HOCH, VMAX)
        else:
            g = max(g - SCHRITT_RUNTER, KRIECHEN)
        geradeaus(g, -1)
        time.sleep_ms(TAKT_MS)
    print("diff zurueck:", impulse_links - impulse_rechts)
    print("Fertig")
finally:
    motoren(0, 0)