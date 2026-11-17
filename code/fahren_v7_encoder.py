# fahren_v7_encoder.py - Wall-Sprint mit Encodern (zaehlen + Strecke), OHNE Drehzahlregelung
# Team Batman, Stand 17.11.2026
# Auf dem ESP32 als main.py speichern.
#
# Ablauf: 3 s warten -> vorwaerts bis die Wand nah ist -> ab BREMSEN_AB bremsen,
# ab 15 cm langsam -> bis der Stossschalter die Wand beruehrt
# -> rueckwaerts dieselbe Strecke (Encoder) -> langsam bis an die Startwand
# (Raeder bleiben stehen) -> aus.
# Encoder: nur zum Messen (Strecke, diff L-R). Geradeaus NUR ueber FAKTOR_LINKS,
# es wird nichts automatisch nachgeregelt.
# Zaehlen die Encoder nicht, faehrt er wie v6 auf Zeit zurueck.
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
enc_links = Pin(25, Pin.IN, Pin.PULL_UP)     # Encoder Motor 2 links, gelb A
enc_rechts = Pin(13, Pin.IN, Pin.PULL_UP)    # Encoder Motor 1 rechts, gelb A

# ----- Drehrichtung -----
# Faehrt ein Rad falsch herum: bei dem Rad 1 <-> -1 tauschen
DREHEN_LINKS = 1
DREHEN_RECHTS = 1

# ----- Geradeaus (ohne Encoder nur hierueber!) -----
ANLAUF = 20                 # unter 20 % dreht kein Rad
FAKTOR_LINKS = 1          # zieht er nach rechts -> kleiner, nach links -> groesser
FAKTOR_LINKS_ZURUECK = 1.05  # dasselbe fuer rueckwaerts

# ----- Fahren -----
VMAX = 80                 # Hoechstgeschwindigkeit in %
KRIECHEN = 15             # Tempo kurz vor der Wand in %
SCHRITT_HOCH = 6          # % schneller pro Takt
SCHRITT_RUNTER = 7        # % langsamer pro Takt
SCHRITT_HOCH_ZURUECK = 7  # % schneller pro Takt beim Rueckwaerts-Anfahren
SCHRITT_RUNTER_ZURUECK = 9  # % langsamer pro Takt beim Rueckwaerts-Bremsen
PAUSE_AN_WAND_MS = 800    # an der Wand warten, bis der Ball in der Schale ruhig liegt,
                          # erst dann rueckwaerts beschleunigen (Ball nicht hin und her ziehen)
BREMSEN_AB = 40           # Echo: ab diesem Abstand in cm bremsen
LANGSAM_AB = 15           # Echo: ab hier nur noch KRIECHEN
WAND_CM = 11              # Echo: Ersatz, falls der Taster beim Start kaputt ist
MIN_ZEIT_MS = 300         # so lange nach dem Losfahren wird keine Wand akzeptiert
TASTER_GEDRUECKT = 1      # was taster.value() liefert, wenn er gedrueckt ist
BREMSEN_AB_ZURUECK = 40   # Encoder: rueckwaerts ab dieser Reststrecke in cm bremsen
                          # (bremst gleichmaessig bis 0 cm Rest, dort steht er)
EXTRA_ZURUECK = 15        # Encoder: so viele cm darf er hinter der Startposition noch suchen
STEHT_MS = 200            # Encoder: Raeder so lange ohne Impuls = Startwand erreicht
CM_PRO_IMPULS = 3.1416 * 8.0 / 224   # Radumfang 8 cm / 224 Impulse pro Umdrehung
# nur ohne Encoder:
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
beruehrt = False          # bleibt True, sobald die Wand einmal erkannt wurde


def wand_beruehrt(abstand):
    # Wand = Stossschalter gedrueckt -> dann rueckwaerts
    # Nur wenn der Taster beim Start kaputt war: Echo unter WAND_CM als Ersatz
    global beruehrt
    if beruehrt:
        return True
    if time.ticks_diff(time.ticks_ms(), fahrt_start) < MIN_ZEIT_MS:
        return False
    if taster_an:
        beruehrt = taster_gedrueckt()
    else:
        beruehrt = abstand <= WAND_CM
    return beruehrt


def melde_wand(phase, d, g):
    # Meldung, sobald der Taster ausloest, und Pruefung, ob es im Kriechtempo kurz vor der Wand war
    if taster_an:
        print(">>> TASTER GEDRUECKT in Phase", phase, "| Echo", round(d), "cm | Tempo", round(g), "%")
    else:
        print(">>> WAND per Echo erkannt in Phase", phase, "| Echo", round(d), "cm | Tempo", round(g), "%")
    fehler = False
    if phase != "BREMSEN":
        print("FEHLER: ausgeloest waehrend der Hinfahrt, noch nicht gebremst!")
        fehler = True
    if g > KRIECHEN + 1:
        print("FEHLER: nicht im Kriechtempo (", round(g), "% statt", KRIECHEN, "%) -> BREMSEN_AB groesser oder SCHRITT_RUNTER groesser")
        fehler = True
    if d > LANGSAM_AB:
        print("FEHLER: nicht kurz vor der Wand (Echo", round(d), "cm > LANGSAM_AB", LANGSAM_AB, "cm) -> Taster loest zu frueh aus / Echo stoert?")
        fehler = True
    if not fehler:
        print("OK: im Kriechtempo kurz vor der Wand")


# ----- Encoder (nur zaehlen, keine Regelung) -----
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


def zeige_diff(richtung):
    # diff > 0: linkes Rad hat sich mehr gedreht als das rechte
    diff = impulse_links - impulse_rechts
    print("diff", richtung, "L-R:", diff, "(L", impulse_links, "R", impulse_rechts, ")")
    if richtung == "hin":
        name = "FAKTOR_LINKS"
    else:
        name = "FAKTOR_LINKS_ZURUECK"
    if diff > 20:
        print("  -> links dreht mehr:", name, "etwas kleiner machen")
    elif diff < -20:
        print("  -> rechts dreht mehr:", name, "etwas groesser machen")


# ----- Hilfen -----
takt = 0


def log(phase, d, g):
    global takt
    takt += 1
    if takt % LOG_JEDER == 0:
        print(phase, "Echo", round(d), "cm | Tempo", round(g), "% | Encoder L", impulse_links, "R", impulse_rechts)


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
    print("Batman v7 mit Encoder (ohne Regelung), VMAX", VMAX)
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
    encoder_null()
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
    gemeldet = False
    if beruehrt:
        stopp()
        melde_wand("HINFAHRT", d, g)
        gemeldet = True
    else:
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
    if not gemeldet:
        melde_wand("BREMSEN", d, g)
    t_hin = sekunden_seit(start)
    strecke = gefahren_cm()
    print("Wand beruehrt nach", t_hin, "s und", round(strecke), "cm")
    print("Warte", PAUSE_AN_WAND_MS, "ms, bis der Ball ruhig ist")
    zeige_diff("hin")
    encoder_ok = strecke > 20
    if not encoder_ok:
        print("ACHTUNG: Encoder zaehlen nicht -> Rueckfahrt auf Zeit")
    time.sleep_ms(PAUSE_AN_WAND_MS)

    # 3. Rueckwaerts: mit Encodern dieselbe Strecke, sonst auf Zeit
    print("Zurueck")
    encoder_null()
    t_zurueck = time.ticks_ms()
    dauer = t_hin * ZURUECK_ANTEIL
    g = 0
    while True:
        if zu_lange(start):
            raise SystemExit
        if encoder_ok:
            rest = strecke - gefahren_cm()
            if rest <= 0:
                break
            # wie an der Wand: je weniger Reststrecke, desto langsamer
            # (gleichmaessig von VMAX bei BREMSEN_AB_ZURUECK auf KRIECHEN bei 0 cm Rest)
            anteil = min(rest / BREMSEN_AB_ZURUECK, 1)
            g_ziel = KRIECHEN + (VMAX - KRIECHEN) * anteil
        else:
            rest_s = dauer - sekunden_seit(t_zurueck)
            if rest_s <= 0:
                break
            rest = 0
            if rest_s < BREMSEN_ZURUECK_S:
                g_ziel = KRIECHEN
            else:
                g_ziel = VMAX
        # hoch hoechstens SCHRITT_HOCH_ZURUECK, runter hoechstens SCHRITT_RUNTER_ZURUECK pro Takt
        g = max(g - SCHRITT_RUNTER_ZURUECK, min(g + SCHRITT_HOCH_ZURUECK, g_ziel))
        fahren(-g)
        log("ZURUECK", rest, g)
        time.sleep_ms(TAKT_MS)
    stopp()
    print("Strecke zurueck erreicht:", round(gefahren_cm()), "von", round(strecke), "cm")
    zeige_diff("zurueck")

    # 4. Langsam rueckwaerts an die Startwand
    print("Startwand suchen")
    if encoder_ok:
        # so lange kriechen, bis die Raeder stehen (Heck an der Wand), hoechstens EXTRA_ZURUECK cm
        ziel = gefahren_cm() + EXTRA_ZURUECK
        letzte = impulse_links + impulse_rechts
        letzte_bewegung = time.ticks_ms()
        while gefahren_cm() < ziel:
            if zu_lange(start):
                raise SystemExit
            fahren(-KRIECHEN)
            time.sleep_ms(TAKT_MS)
            jetzt = impulse_links + impulse_rechts
            if jetzt != letzte:
                letzte = jetzt
                letzte_bewegung = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), letzte_bewegung) > STEHT_MS:
                print("Startwand erreicht (Raeder stehen)")
                break
    else:
        fahren(-KRIECHEN)
        time.sleep(SUCHEN_S)
    stopp()
    print("Fertig nach", sekunden_seit(start), "s")
except SystemExit:
    pass
finally:
    stopp()