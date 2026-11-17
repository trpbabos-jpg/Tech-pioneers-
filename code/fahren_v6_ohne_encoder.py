# fahren_v6_ohne_encoder.py - Wall-Sprint OHNE Encoder / Drehzahlregelung
# Team Batman, Stand 17.11.2026
# Auf dem ESP32 als main.py speichern.
#
# Ablauf: 3 s warten -> vorwaerts bis die Wand nah ist -> ab 50 cm bremsen,
# ab 15 cm langsam -> bis der Stossschalter die Wand beruehrt
# -> rueckwaerts auf Zeit (so lange wie hin) -> langsam bis an die Startwand -> aus.
# Geradeaus nur ueber FAKTOR_LINKS (keine Korrektur waehrend der Fahrt).
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

# ----- Drehrichtung -----
# Faehrt ein Rad falsch herum: bei dem Rad 1 <-> -1 tauschen
DREHEN_LINKS = 1
DREHEN_RECHTS = 1

# ----- Geradeaus (ohne Encoder nur hierueber!) -----
ANLAUF = 20                 # unter 20 % dreht kein Rad
FAKTOR_LINKS = 0.9          # zieht er nach rechts -> kleiner, nach links -> groesser
FAKTOR_LINKS_ZURUECK = 0.95 # rueckwaerts: zieht er nach links -> groesser (17.11.: 0.9 zog links)

# ----- Fahren -----
VMAX = 80                 # Hoechstgeschwindigkeit in %
KRIECHEN = 30             # Tempo kurz vor der Wand in %
SCHRITT_HOCH = 6          # % schneller pro Takt
SCHRITT_RUNTER = 7        # % langsamer pro Takt
SCHRITT_HOCH_ZURUECK = 2  # % schneller pro Takt beim Rueckwaerts-Anfahren (17.11.: 6 war zu ruckig)
PAUSE_AN_WAND_MS = 800    # so lange an der Wand stehen, bevor er zurueckfaehrt
BREMSEN_AB = 50           # Echo: ab diesem Abstand in cm bremsen
LANGSAM_AB = 15           # Echo: ab hier nur noch KRIECHEN
WAND_CM = 11              # Echo: Ersatz, falls der Taster beim Start kaputt ist
MIN_ZEIT_MS = 300         # so lange nach dem Losfahren wird keine Wand akzeptiert
TASTER_GEDRUECKT = 1      # was taster.value() liefert, wenn er gedrueckt ist
ZURUECK_ANTEIL = 1.3      # Rueckfahrzeit = Hinfahrzeit * diesen Wert (zu kurz -> groesser)
                          # 1.3 weil er rueckwaerts langsamer anfaehrt
BREMSEN_ZURUECK_S = 0.8   # die letzten 0,8 s der Rueckfahrt abbremsen
SUCHEN_S = 1.5            # danach so lange langsam rueckwaerts an die Startwand
TAKT_MS = 50
LOG_JEDER = 4             # jeden 4. Takt Messwerte in die Shell
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


def fahren(g):
    # g > 0 vorwaerts, g < 0 rueckwaerts, beide Raeder gleich (links mit Faktor)
    if g >= 0:
        motor(m2a, m2b, DREHEN_LINKS * g * FAKTOR_LINKS)
    else:
        motor(m2a, m2b, DREHEN_LINKS * g * FAKTOR_LINKS_ZURUECK)
    motor(m1a, m1b, DREHEN_RECHTS * g)


def stopp():
    fahren(0)


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


fahrt_start = 0


def wand_beruehrt(abstand):
    # Wand = Stossschalter gedrueckt -> dann rueckwaerts
    # Nur wenn der Taster beim Start kaputt war: Echo unter WAND_CM als Ersatz
    if time.ticks_diff(time.ticks_ms(), fahrt_start) < MIN_ZEIT_MS:
        return False
    if taster_an:
        return taster_gedrueckt()
    return abstand <= WAND_CM


# ----- Hilfen -----
takt = 0


def log(phase, d, g):
    global takt
    takt += 1
    if takt % LOG_JEDER == 0:
        print(phase, "Echo", round(d), "cm | Tempo", round(g), "%")


def sekunden_seit(t):
    return time.ticks_diff(time.ticks_ms(), t) / 1000


def zu_lange(start):
    if time.ticks_diff(time.ticks_ms(), start) > MAX_FAHRZEIT_MS:
        print("Abbruch: zu lange gefahren")
        return True
    return False


# ----- Ablauf -----
try:
    stopp()
    print("Batman v6 ohne Encoder, VMAX", VMAX)
    if taster_gedrueckt():
        taster_an = False
        print("ACHTUNG: Stossschalter meldet schon gedrueckt -> wird ignoriert, Wand nur per Echo")
    for i in range(3):
        print("Echo vorne beim Start:", round(messen()), "cm")
        time.sleep_ms(100)
    time.sleep(3)                     # Regel: 2 bis 10 s an der Startwand
    start = time.ticks_ms()
    fahrt_start = start

    # 1. Hinfahren: sanft schneller bis VMAX, bis die Wand nah ist
    print("Hinfahren")
    g = 0
    d = median.neu(messen())
    while d > BREMSEN_AB and not wand_beruehrt(d):
        if zu_lange(start):
            raise SystemExit
        g = min(g + SCHRITT_HOCH, VMAX)
        fahren(g)
        log("HIN", d, g)
        time.sleep_ms(TAKT_MS)
        d = median.neu(messen())
    print("Wand nah bei", round(d), "cm")

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
        fahren(g)
        log("BREMS", d, g)
        time.sleep_ms(TAKT_MS)
        d = median.neu(messen())
    stopp()
    t_hin = sekunden_seit(start)
    print("Wand beruehrt nach", t_hin, "s")
    time.sleep_ms(PAUSE_AN_WAND_MS)

    # 3. Rueckwaerts auf Zeit, die letzten BREMSEN_ZURUECK_S langsamer
    print("Zurueck")
    t_zurueck = time.ticks_ms()
    dauer = t_hin * ZURUECK_ANTEIL
    g = 0
    while sekunden_seit(t_zurueck) < dauer:
        if zu_lange(start):
            raise SystemExit
        if dauer - sekunden_seit(t_zurueck) < BREMSEN_ZURUECK_S:
            g = max(g - SCHRITT_RUNTER, KRIECHEN)
        else:
            g = min(g + SCHRITT_HOCH_ZURUECK, VMAX)
        fahren(-g)
        log("ZURUECK", 0, g)
        time.sleep_ms(TAKT_MS)

    # 4. Langsam rueckwaerts an die Startwand
    print("Startwand suchen")
    fahren(-KRIECHEN)
    time.sleep(SUCHEN_S)
    stopp()
    print("Fertig nach", sekunden_seit(start), "s")
except SystemExit:
    pass
finally:
    stopp()
