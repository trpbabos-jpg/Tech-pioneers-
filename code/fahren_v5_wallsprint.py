# fahren_v5_wallsprint.py - Wall-Sprint komplett
# Team Batman, Stand 17.11.2026
# Auf dem ESP32 als main.py speichern.
#
# Ablauf: 3 s warten -> vorwaerts bis die Wand nah ist -> ab 50 cm bremsen,
# ab 15 cm langsam -> Wand beruehren (Stossschalter, Reserve: Echo 11 cm)
# -> rueckwaerts die gleiche Strecke -> langsam bis an die Startwand
# (Raeder bleiben stehen) -> aus.
# Falsche Drehrichtung? -> DREHEN_LINKS / DREHEN_RECHTS aendern.

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

# ----- Drehrichtung -----
# Faehrt ein Rad falsch herum: bei dem Rad 1 <-> -1 tauschen
# Test 17.11. nachmittags: mit -1 / -1 fuhr er rueckwaerts -> jetzt 1 / 1
DREHEN_LINKS = 1
DREHEN_RECHTS = 1

# ----- Gemessen mit kalibrieren.py und drehzahl_test.py -----
ANLAUF = 20                 # unter 20 % dreht kein Rad
FAKTOR_LINKS = 0.7          # motorkraft links vorwaerts
FAKTOR_LINKS_ZURUECK = 0.7  # motorkraft links rueckwaerts

# ----- Fahren (Werte aus main.py, 03.11.) -----
VMAX = 80                 # Hoechstgeschwindigkeit in %
KRIECHEN = 20             # Tempo kurz vor der Wand in %
SCHRITT_HOCH = 6          # % schneller pro Takt
SCHRITT_RUNTER = 7        # % langsamer pro Takt
BREMSEN_AB = 50           # Echo: ab diesem Abstand in cm bremsen
LANGSAM_AB = 15           # Echo: ab hier nur noch KRIECHEN
WAND_CM = 11              # Echo: Wand erreicht (Echo sitzt ca. 10 cm hinter dem Stossschalter)
MIN_STRECKE = 100         # cm: vorher wird keine Wand akzeptiert (Bahn ist 200 cm)
TASTER_GEDRUECKT = 1      # was taster.value() liefert, wenn er gedrueckt ist
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
    # positiv = vorwaerts. Falsche Richtung? -> oben DREHEN_LINKS / DREHEN_RECHTS aendern
    if links >= 0:
        motor(m2a, m2b, DREHEN_LINKS * links * FAKTOR_LINKS)
    else:
        motor(m2a, m2b, DREHEN_LINKS * links * FAKTOR_LINKS_ZURUECK)
    motor(m1a, m1b, DREHEN_RECHTS * rechts)


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
taster_an = True          # wird beim Start abgeschaltet, wenn er schon "gedrueckt" meldet


def taster_gedrueckt():
    # 7-mal nachschauen, damit kurzes Zucken beim Fahren nicht ausloest
    if not taster_an:
        return False
    for i in range(7):
        if taster.value() != TASTER_GEDRUECKT:
            return False
        time.sleep_ms(2)
    return True


def wand_beruehrt(abstand):
    # Wand = Stossschalter gedrueckt ODER Echo sehr nah,
    # aber erst nach MIN_STRECKE (sonst stoert z. B. ein Echo vom eigenen Aufbau)
    if gefahren_cm() < MIN_STRECKE:
        return False
    return taster_gedrueckt() or abstand <= WAND_CM


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
    if taster_gedrueckt():
        taster_an = False
        print("ACHTUNG: Stossschalter meldet schon gedrueckt -> wird ignoriert, Wand nur per Echo")
    for i in range(3):
        print("Echo vorne beim Start:", round(messen()), "cm")
        time.sleep_ms(100)
    time.sleep(3)                     # Regel: 2 bis 10 s an der Startwand
    start = time.ticks_ms()

    # 1. Hinfahren: sanft schneller bis VMAX, bis die Wand nah ist
    print("Hinfahren")
    encoder_null()
    g = 0
    d = median.neu(messen())
    while (d > BREMSEN_AB or gefahren_cm() < MIN_STRECKE - BREMSEN_AB) and not wand_beruehrt(d):
        if zu_lange(start):
            raise SystemExit
        g = min(g + SCHRITT_HOCH, VMAX)
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
        d = median.neu(messen())
    print("Wand nah bei", round(d), "cm")
    print("diff hin:", impulse_links - impulse_rechts)

    # 2. Sanft bremsen auf Kriechtempo, bis der Taster die Wand beruehrt
    print("Bremsen")
    while not wand_beruehrt(d):
        if zu_lange(start):
            raise SystemExit
        if d > LANGSAM_AB:
            # zwischen BREMSEN_AB und LANGSAM_AB gleichmaessig auf KRIECHEN
            anteil = (d - LANGSAM_AB) / (BREMSEN_AB - LANGSAM_AB)
            g_ziel = KRIECHEN + (VMAX - KRIECHEN) * min(anteil, 1)
        else:
            g_ziel = KRIECHEN       # ab 15 cm nur noch langsam
        g = max(g - SCHRITT_RUNTER, min(g, g_ziel))
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
        d = median.neu(messen())
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
