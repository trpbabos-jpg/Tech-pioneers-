# fahren_v4_ball.py - Anfahren und Bremsen mit Ball testen + kompletter Wall-Sprint
# Team Batman, Stand 17.11.2026 (noch nicht getestet)
# Auf dem ESP32 als main.py speichern.
#
# Neu gegenueber main.py (03.11.):
# - MODUS "ANFAHREN": nur anfahren, Teststrecke fahren, sanft bremsen. Ohne Wand,
#   zum Ausprobieren, ob der Ball in der Schale bleibt.
# - Anfahren als S-Kurve ueber eine feste Zeit (kein Ruck am Anfang und am Ende)
# - Bremsen mit Wurzel-Profil = gleichmaessige Verzoegerung (schont den Ball)
# - Rueckfahrt endet erst, wenn die Raeder an der Startwand stehen bleiben
# - Shell-Ausgabe: Abstand, Tempo in %, Geschwindigkeit in cm/s, Beschleunigung in cm/s^2

from machine import Pin, PWM, time_pulse_us
import time

# ===================== MODUS =====================
# "ANFAHREN" : anfahren, STRECKE_TEST cm fahren, sanft anhalten (Ball-Test, keine Wand noetig)
# "WAND"     : Wall-Sprint komplett: hin, sanft an die Wand, zurueck zur Startwand
MODUS = "ANFAHREN"
STRECKE_TEST = 100        # cm, nur fuer MODUS "ANFAHREN"
LOG = True                # Messwerte in der Shell ausgeben

# ===================== PINS (pinbelegung.md, Stand 29.10.) =====================
m1a = PWM(Pin(14), freq=20000, duty_u16=0)   # Motor 1 rechts
m1b = PWM(Pin(27), freq=20000, duty_u16=0)
m2a = PWM(Pin(33), freq=20000, duty_u16=0)   # Motor 2 links
m2b = PWM(Pin(32), freq=20000, duty_u16=0)
trig = Pin(19, Pin.OUT, value=0)             # HC-SR04 vorne
echo = Pin(35, Pin.IN)                       # ueber Spannungsteiler 1k / 2,2k
taster = Pin(22, Pin.IN, Pin.PULL_UP)        # Stossschalter vorne (Oeffner: gedrueckt = 1)
enc_links = Pin(25, Pin.IN, Pin.PULL_UP)     # Encoder Motor 2, gelb A
enc_rechts = Pin(13, Pin.IN, Pin.PULL_UP)    # Encoder Motor 1, gelb A

# ===================== KALIBRIERT (einstellwerte.md) =====================
ANLAUF = 20                 # unter 20 % dreht kein Rad
FAKTOR_LINKS = 0.7          # linker Motor vorwaerts
FAKTOR_LINKS_ZURUECK = 0.7  # linker Motor rueckwaerts
CM_PRO_IMPULS = 3.1416 * 8.0 / 224   # Radumfang 8 cm / 224 Impulse

# ===================== FAHREN (mit Ball ausprobieren) =====================
VMAX = 60                 # Hoechsttempo in %. Erst mit 60 testen, dann hoch
KRIECHEN = 20             # Tempo beim Beruehren der Wand in %
ANFAHR_ZEIT_MS = 1500     # 0 -> VMAX dauert so lange. Ball rollt raus -> groesser machen
BREMSEN_AB = 60           # cm (Echo vorne): ab hier bremsen
STOPP_ABSTAND = 15        # cm (Echo vorne): hier ist KRIECHEN erreicht
                          # Echo sitzt ca. 10 cm hinter dem Stossschalter
BREMSEN_AB_ZURUECK = 45   # cm Reststrecke rueckwaerts: ab hier bremsen
MAX_RUNTER = 4            # hoechstens so viele % langsamer pro Takt (Ball!)
TAKT_MS = 50
KP = 0.5                  # Encoder-Korrektur Geradeausfahrt
MAX_FAHRZEIT_MS = 30000   # Sicherheit: nach 30 s alles aus


# ===================== MOTOREN (Kap. 4b) =====================
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
    if links >= 0:
        motor(m2a, m2b, links * FAKTOR_LINKS)
    else:
        motor(m2a, m2b, links * FAKTOR_LINKS_ZURUECK)
    motor(m1a, m1b, -rechts)      # rechter Motor ist gespiegelt eingebaut


def stopp():
    motoren(0, 0)


# ===================== ULTRASCHALL VORNE (Kap. 4a) =====================
def messen():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400                # kein Echo = weit weg
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


# ===================== TASTER (Kap. 4c) =====================
def wand_beruehrt():
    # 7-mal nachschauen, damit Zucken beim Fahren nicht ausloest
    for i in range(7):
        if taster.value() != 1:
            return False
        time.sleep_ms(2)
    return True


# ===================== ENCODER =====================
impulse_links = 0
impulse_rechts = 0


def zaehle_links(pin):
    global impulse_links
    impulse_links += 1


def zaehle_rechts(pin):
    global impulse_rechts
    impulse_rechts += 1


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
    grenze = 8 * g / VMAX if VMAX > 0 else 0
    korrektur = max(-grenze, min(grenze, korrektur))
    motoren((g - korrektur) * richtung, (g + korrektur) * richtung)


# ===================== PROFILE (Ball-schonend) =====================
def s_kurve(t_ms):
    # 0 -> 1 ueber ANFAHR_ZEIT_MS, sanft am Anfang und am Ende (smoothstep)
    x = t_ms / ANFAHR_ZEIT_MS
    if x >= 1:
        return 1.0
    if x <= 0:
        return 0.0
    return x * x * (3 - 2 * x)


def brems_tempo(rest_cm, brems_strecke):
    # Wurzel-Profil: v ~ Wurzel(Reststrecke) -> gleichmaessige Verzoegerung
    if rest_cm <= 0:
        return KRIECHEN
    anteil = min(rest_cm / brems_strecke, 1.0)
    return KRIECHEN + (VMAX - KRIECHEN) * (anteil ** 0.5)


# ===================== LOG =====================
class Logger:
    # rechnet aus den Encodern Geschwindigkeit und Beschleunigung aus
    def __init__(self):
        self.t_alt = time.ticks_ms()
        self.s_alt = gefahren_cm()
        self.v_alt = 0
        self.a_max = 0

    def schreibe(self, phase, abstand, g):
        jetzt = time.ticks_ms()
        dt = time.ticks_diff(jetzt, self.t_alt) / 1000
        if dt <= 0:
            return
        s = gefahren_cm()
        v = (s - self.s_alt) / dt
        a = (v - self.v_alt) / dt
        if abs(a) > abs(self.a_max):
            self.a_max = a
        self.t_alt, self.s_alt, self.v_alt = jetzt, s, v
        if LOG:
            print("{} d={:.0f}cm g={:.0f}% v={:.0f}cm/s a={:.0f}cm/s2 s={:.0f}cm".format(
                phase, abstand, g, v, a, s))

    def neu_start(self):
        self.t_alt = time.ticks_ms()
        self.s_alt = gefahren_cm()
        self.v_alt = 0


# ===================== ABLAEUFE =====================
def zeit_ueberschritten(start):
    return time.ticks_diff(time.ticks_ms(), start) > MAX_FAHRZEIT_MS


def test_anfahren():
    # Ball-Test: S-Kurve hoch, Strecke fahren, mit Wurzel-Profil auf 0 bremsen
    print("== Test Anfahren: {} cm, VMAX {} %, Anfahrzeit {} ms ==".format(
        STRECKE_TEST, VMAX, ANFAHR_ZEIT_MS))
    encoder_null()
    log = Logger()
    start = time.ticks_ms()
    g = 0
    brems_strecke = BREMSEN_AB - STOPP_ABSTAND

    while True:
        rest = STRECKE_TEST - gefahren_cm()
        if rest <= 0 or wand_beruehrt() or zeit_ueberschritten(start):
            break
        t = time.ticks_diff(time.ticks_ms(), start)
        g_ziel = VMAX * s_kurve(t)
        if rest < brems_strecke:
            # zum Schluss bis fast 0 runter statt Kriechen (Wurzel-Profil)
            g_ziel = min(g_ziel, max(VMAX * (rest / brems_strecke) ** 0.5, 3))
        g = max(g - MAX_RUNTER, g_ziel)  # nie schneller langsamer werden als MAX_RUNTER
        geradeaus(g, 1)
        log.schreibe("TEST", rest, g)
        time.sleep_ms(TAKT_MS)

    # letzte Prozent sanft auslaufen lassen
    while g > 0:
        g = max(g - MAX_RUNTER, 0)
        geradeaus(g, 1)
        time.sleep_ms(TAKT_MS)
    stopp()
    print("Fertig: {:.0f} cm, diff L-R = {}, staerkste Beschl. = {:.0f} cm/s2".format(
        gefahren_cm(), impulse_links - impulse_rechts, log.a_max))


def wall_sprint():
    start = time.ticks_ms()
    log = Logger()

    # ---- 1. Hinfahren: S-Kurve bis VMAX, bis die Wand nah ist ----
    print("== Hinfahren ==")
    encoder_null()
    log.neu_start()
    g = 0
    t0 = time.ticks_ms()
    d = median.neu(messen())
    while d > BREMSEN_AB and not wand_beruehrt():
        if zeit_ueberschritten(start):
            return
        g = VMAX * s_kurve(time.ticks_diff(time.ticks_ms(), t0))
        geradeaus(g, 1)
        log.schreibe("HIN", d, g)
        time.sleep_ms(TAKT_MS)
        d = median.neu(messen())

    # ---- 2. Sanft bremsen bis der Stossschalter die Wand beruehrt ----
    print("== Bremsen ==")
    brems_strecke = BREMSEN_AB - STOPP_ABSTAND
    while not wand_beruehrt():
        if zeit_ueberschritten(start):
            return
        d = median.neu(messen())
        g_ziel = brems_tempo(d - STOPP_ABSTAND, brems_strecke)
        g = max(g - MAX_RUNTER, min(g, g_ziel))
        geradeaus(g, 1)
        log.schreibe("BREMS", d, g)
        time.sleep_ms(TAKT_MS)
    stopp()
    strecke = gefahren_cm()
    print("Wand beruehrt nach {:.0f} cm, diff L-R = {}".format(
        strecke, impulse_links - impulse_rechts))
    time.sleep_ms(300)

    # ---- 3. Rueckwaerts: S-Kurve hoch, vor dem Ziel bremsen ----
    print("== Zurueck ==")
    encoder_null()
    log.neu_start()
    g = 0
    t0 = time.ticks_ms()
    while True:
        rest = strecke - gefahren_cm()
        if rest <= 3:
            break
        if zeit_ueberschritten(start):
            return
        g_hoch = VMAX * s_kurve(time.ticks_diff(time.ticks_ms(), t0))
        g_ziel = min(g_hoch, brems_tempo(rest, BREMSEN_AB_ZURUECK))
        g = max(g - MAX_RUNTER, g_ziel)
        geradeaus(g, -1)
        log.schreibe("ZURUECK", rest, g)
        time.sleep_ms(TAKT_MS)

    # ---- 4. Kriechend bis an die Startwand (Raeder bleiben stehen) ----
    print("== Startwand suchen ==")
    letzte_impulse = impulse_links + impulse_rechts
    letzte_bewegung = time.ticks_ms()
    extra_start = gefahren_cm()
    while gefahren_cm() - extra_start < 15:       # hoechstens 15 cm extra
        if zeit_ueberschritten(start):
            return
        geradeaus(KRIECHEN, -1)
        time.sleep_ms(TAKT_MS)
        jetzt_impulse = impulse_links + impulse_rechts
        if jetzt_impulse != letzte_impulse:
            letzte_impulse = jetzt_impulse
            letzte_bewegung = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), letzte_bewegung) > 200:
            print("Startwand erreicht (Raeder stehen)")
            break
    stopp()
    print("Fertig nach {:.1f} s, diff zurueck L-R = {}".format(
        time.ticks_diff(time.ticks_ms(), start) / 1000, impulse_links - impulse_rechts))


# ===================== START =====================
try:
    stopp()
    print("Batman v4, Modus:", MODUS)
    time.sleep(3)          # Regel: 2 bis 10 s an der Startwand bleiben
    if MODUS == "ANFAHREN":
        test_anfahren()
    else:
        wall_sprint()
finally:
    stopp()
