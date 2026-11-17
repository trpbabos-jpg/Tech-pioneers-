# fahren_v5_wallsprint.py - Wall-Sprint komplett mit den Werten aus main.py (03.11.)
# Team Batman, Stand 17.11.2026 (noch nicht getestet)
# Auf dem ESP32 als main.py speichern.
#
# Ablauf: 3 s warten -> hin bis die Wand nah ist -> sanft bremsen bis der
# Stossschalter beruehrt -> rueckwaerts die gleiche Strecke -> kriechend bis
# an die Startwand (Raeder bleiben stehen) -> aus.
# Unterschied zu main.py: Schritt 4 (Startwand sicher beruehren) und Fahrzeit-Ausgabe.

from machine import Pin, PWM, time_pulse_us
import time

# ----- Pins (pinbelegung.md, Stand 29.10.) -----
m1a = PWM(Pin(14), freq=20000, duty_u16=0)   # Motor rechts
m1b = PWM(Pin(27), freq=20000, duty_u16=0)
m2a = PWM(Pin(33), freq=20000, duty_u16=0)   # Motor links
m2b = PWM(Pin(32), freq=20000, duty_u16=0)
trig = Pin(19, Pin.OUT, value=0)             # HC-SR04 vorne
echo = Pin(35, Pin.IN)                       # ueber Spannungsteiler
taster = Pin(22, Pin.IN, Pin.PULL_UP)        # Stossschalter vorne
enc_links = Pin(25, Pin.IN, Pin.PULL_UP)
enc_rechts = Pin(13, Pin.IN, Pin.PULL_UP)

# ----- Gemessen mit kalibrieren.py und drehzahl_test.py -----
ANLAUF = 20                 # unter 20 % dreht kein Rad
FAKTOR_LINKS = 0.7          # motorkraft links vorwaerts
FAKTOR_LINKS_ZURUECK = 0.7  # motorkraft links rueckwaerts

# ----- Fahren (Werte aus main.py, 03.11.) -----
VMAX = 80                 # Hoechstgeschwindigkeit in %
KRIECHEN = 20             # Tempo kurz vor der Wand in %
SCHRITT_HOCH = 6          # % schneller pro Takt
SCHRITT_RUNTER = 7        # % langsamer pro Takt
BREMSEN_AB = 50           # ab diesem Abstand in cm bremsen
BREMSEN_AB_ZURUECK = 45   # rueckwaerts: ab dieser Reststrecke in cm bremsen
TAKT_MS = 50
KP = 0.5                  # Encoder-Korrektur fuer die Geradeausfahrt
CM_PRO_IMPULS = 3.1416 * 8.0 / 224   # Radumfang / Impulse pro Umdrehung
EXTRA_ZURUECK = 15        # cm: so weit darf er hinter der Startposition noch suchen
STEHT_MS = 200            # Raeder so lange ohne Impuls = Startwand erreicht
MAX_FAHRZEIT_MS = 60000   # Sicherheit (Regel: 90 s)


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
    # Test 17.11.: bei beiden Motoren A = rueckwaerts, B = vorwaerts
    # -> beide Seiten umdrehen, damit positiv = vorwaerts
    if links >= 0:
        motor(m2a, m2b, -links * FAKTOR_LINKS)
    else:
        motor(m2a, m2b, -links * FAKTOR_LINKS_ZURUECK)
    motor(m1a, m1b, -rechts)


# ----- Ultraschall (Kap. 4a) -----
def messen():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400
    return laufzeit * 0.0343 / 2


class Median:
    # mittlere von 3 Messungen, eine Fehlmessung stoert nicht (Kap. 4d)
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


# ----- Encoder -----
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


def encoder_null():
    global impulse_links, impulse_rechts
    impulse_links = 0
    impulse_rechts = 0


def gefahren_cm():
    return (impulse_links + impulse_rechts) / 2 * CM_PRO_IMPULS


def geradeaus(g, richtung):
    # Rad mit mehr Impulsen ist weiter gefahren -> etwas langsamer
    korrektur = KP * (impulse_links - impulse_rechts)
    grenze = 8 * g / VMAX       # bei VMAX hoechstens 8 %, langsamer weniger
    korrektur = max(-grenze, min(grenze, korrektur))
    motoren((g - korrektur) * richtung, (g + korrektur) * richtung)


def zu_lange(start):
    if time.ticks_diff(time.ticks_ms(), start) > MAX_FAHRZEIT_MS:
        print("Abbruch: zu lange gefahren")
        return True
    return False


# ----- Ablauf -----
try:
    motoren(0, 0)
    print("Batman v5 Wall-Sprint, VMAX", VMAX)
    time.sleep(3)                     # Regel: 2 bis 10 s an der Startwand
    start = time.ticks_ms()

    # 1. Hinfahren: sanft schneller bis VMAX, bis die Wand nah ist
    print("Hinfahren")
    encoder_null()
    g = 0
    while median.neu(messen()) > BREMSEN_AB and not wand_beruehrt():
        if zu_lange(start):
            raise SystemExit
        g = min(g + SCHRITT_HOCH, VMAX)
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
    print("diff hin:", impulse_links - impulse_rechts)

    # 2. Sanft bremsen auf Kriechtempo, bis der Taster die Wand beruehrt
    print("Bremsen")
    while not wand_beruehrt():
        if zu_lange(start):
            raise SystemExit
        g = max(g - SCHRITT_RUNTER, KRIECHEN)
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
    motoren(0, 0)
    strecke = gefahren_cm()
    t_wand = time.ticks_diff(time.ticks_ms(), start) / 1000
    print("Wand beruehrt nach", round(strecke), "cm und", t_wand, "s")
    time.sleep_ms(500)

    # 3. Rueckwaerts dieselbe Strecke zurueck, am Ende wieder sanft
    print("Zurueck")
    encoder_null()
    g = 0
    while gefahren_cm() < strecke:
        if zu_lange(start):
            raise SystemExit
        if strecke - gefahren_cm() > BREMSEN_AB_ZURUECK:
            g = min(g + SCHRITT_HOCH, VMAX)
        else:
            g = max(g - SCHRITT_RUNTER, KRIECHEN)
        geradeaus(g, -1)
        time.sleep_ms(TAKT_MS)
    print("diff zurueck:", impulse_links - impulse_rechts)

    # 4. Kriechend weiter, bis das Heck an der Startwand ist (Raeder stehen)
    print("Startwand suchen")
    ziel = gefahren_cm() + EXTRA_ZURUECK
    letzte = impulse_links + impulse_rechts
    letzte_bewegung = time.ticks_ms()
    while gefahren_cm() < ziel:
        if zu_lange(start):
            raise SystemExit
        geradeaus(KRIECHEN, -1)
        time.sleep_ms(TAKT_MS)
        jetzt = impulse_links + impulse_rechts
        if jetzt != letzte:
            letzte = jetzt
            letzte_bewegung = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), letzte_bewegung) > STEHT_MS:
            print("Startwand erreicht")
            break
    motoren(0, 0)
    print("Fertig nach", time.ticks_diff(time.ticks_ms(), start) / 1000, "s")
except SystemExit:
    pass
finally:
    motoren(0, 0)
