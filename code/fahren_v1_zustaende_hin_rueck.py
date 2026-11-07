# main.py - Wettbewerbsprogramm Wall-Sprint (Hinfahrt und Rueckfahrt)
# Team Batman
#
# Ablauf (Zustaende):
#   WARTEN           3 s an der Startwand stehen bleiben (Regel: mind. 2 s, hoechstens 10 s)
#   HINFAHREN        sanft anfahren und geradeaus fahren (Encoder-Korrektur)
#   BREMSEN          vor der Endwand langsam werden bis Kriechtempo (Ultraschall)
#   AN_DER_WAND      Stossschalter beruehrt die Wand -> kurz stehen bleiben
#   ZURUECK          rueckwaerts geradeaus zur Startwand (ohne Umdrehen)
#   ZURUECK_BREMSEN  vor der Startwand langsam werden (Reststrecke aus den Encodern)
#   AM_START         Startwand erreicht: die Raeder drehen nicht mehr -> Stopp
#   FERTIG           Programm ist zu Ende
#
# Rueckfahrt: Hinten ist kein Ultraschall. Deshalb merkt sich der Roboter auf der
# Hinfahrt die Strecke (Encoder-Impulse) und faehrt genau diese Strecke zurueck.
# Die Startwand erkennt er daran, dass beim Kriechen keine Impulse mehr kommen.
#
# Start: Wippschalter an -> ESP32 startet -> main.py laeuft von selbst.
#
# SO TESTET IHR:
#   1. Vorher ultraschall_test.py, motor_test.py, taster_test.py und
#      drehzahl_test.py laufen lassen und die Werte unten eintragen.
#   2. Erst OHNE Ball testen, mit einem Karton als Wand.
#   3. In Thonny starten: nach 3 s faehrt er los! Platz machen.
#   4. In der Shell steht bei jedem Takt Zustand, Abstand, Geschwindigkeit und Korrektur.
#   5. Wenn alles klappt: als main.py auf den ESP32 speichern.

from machine import Pin, PWM, time_pulse_us
import time

# ---------- Pins (aus unserem Steckplan) ----------
M2B, M2A = 32, 33         # Motor 2, links
M1B, M1A = 27, 14         # Motor 1, rechts
ENC2_A, ENC2_B = 25, 26   # Encoder Motor 2, links (Phase B nutzen wir noch nicht)
ENC1_A, ENC1_B = 13, 4    # Encoder Motor 1, rechts (Phase B nutzen wir noch nicht)
TRIG = 19
ECHO = 35                 # nur Eingang, ohne Pull-up
TASTER = 22

# ---------- Motoren als Allererstes auf 0 ----------
# GPIO14 gibt beim Hochfahren kurz ein Signal aus, deshalb sofort duty 0
m1a = PWM(Pin(M1A), freq=20000, duty_u16=0)
m1b = PWM(Pin(M1B), freq=20000, duty_u16=0)
m2a = PWM(Pin(M2A), freq=20000, duty_u16=0)
m2b = PWM(Pin(M2B), freq=20000, duty_u16=0)

# ---------- Einstellungen ----------
TASTER_GEDRUECKT = 1      # mit taster_test.py pruefen! (Oeffner laut Kap. 4c: 1)
TASTER_LESEN = 5          # so oft wird der Taster pro Takt gelesen (alle 2 ms)
TASTER_TAKTE = 1          # so viele Takte hintereinander muss er gedrueckt sein (29.10.: 1 klappt besser als 2)
# 29.10.: Beim Fahren hat der Taster ohne Wand ausgeloest (Ruetteln / Wackelkontakt).
# Deshalb zaehlt er erst als gedrueckt, wenn er laenger als ein kurzes Zucken gedrueckt bleibt.

RICHTUNG_LINKS = 1       # Testtaste M2A am MDD3A dreht links vorwaerts
RICHTUNG_RECHTS = -1     # Motor rechts ist gespiegelt eingebaut (Kabel: M1A an 14, M1B an 27)

STARTWARTEN_MS = 3000     # so lange bleibt er an der Startwand stehen
ZYKLUS_MS = 50            # fester Takt wie in Kap. 4d (50 ms = 20 Hz)
DT = ZYKLUS_MS / 1000     # in Sekunden

ANLAUF_LINKS = 20         # 29.10. kalibrieren.py in der Luft: links dreht ab 20 %
ANLAUF_RECHTS = 20        # 29.10.: gemessen 16 %, aber gleicher Wert wie links laeuft gleichmaessiger (drehzahl_test.py)
FAKTOR_LINKS = 0.94       # 29.10. drehzahl_test.py in der Luft: links ca. 4-5 % schneller
START = 5                 # damit faengt er an
VMAX = 50                 # selbst messen! in %
KRIECHEN = 15             # Kriechtempo vor der Wand in % (nach neuer Kalibrierung anpassen)
SCHRITT_HOCH = 2          # so viel % schneller pro Takt (sanft anfahren)
SCHRITT_RUNTER = 3        # so viel % langsamer pro Takt (sanft bremsen)

BREMSEN_AB = 60           # selbst messen! ab diesem Abstand in cm wird gebremst
RESTZEIT_S = 1.0          # oder wenn er in weniger als 1 s an der Wand waere (Kap. 4d)
MAX_GESCHW_CMS = 120      # gemessen max. ca. 85 cm/s bei 100 %, groessere Werte sind Messfehler
MAX_KRIECHZEIT_MS = 8000  # Sicherheit: so lange darf er hoechstens kriechen

# ---------- Rueckfahrt ----------
PAUSE_AN_WAND_MS = 500    # so lange bleibt er an der Endwand stehen, bevor er zurueckfaehrt
VMAX_ZURUECK = 50         # in %, rueckwaerts
BREMSEN_AB_ZURUECK = 50   # ab dieser Reststrecke in cm (laut Encoder) wird gebremst
STILLSTAND_TAKTE = 3      # so viele Takte fast ohne Impulse beim Kriechen = Startwand erreicht
MIN_IMPULSE_TAKT = 4      # beide Raeder zusammen, Kriechen sind sonst ca. 15-20 pro Takt
MAX_UEBERFAHREN_CM = 15   # Sicherheit: hoechstens so viel weiter als die Hinfahrt
IMPULSE_PRO_UMDREHUNG = 224   # Kap. 4b, Folie 23
RAD_DURCHMESSER = 8.0         # in cm
CM_PRO_IMPULS = 3.1416 * RAD_DURCHMESSER / IMPULSE_PRO_UMDREHUNG

KP = 0.5                  # selbst ausprobieren! Korrektur in % pro Impuls Unterschied
MAX_KORREKTUR = 8         # hoechstens so viel % Korrektur
# KRIECHEN - MAX_KORREKTUR muss groesser als 0 sein, sonst bleibt ein Rad stehen

MIN_CM = 2                # Messbereich HC-SR04 (Kap. 4d)
MAX_CM = 400


# ---------- Hilfsfunktion aus Kap. 4d ----------
def begrenzen(x, unten, oben):
    return max(unten, min(oben, x))


# ---------- Motoren (wie motor() aus Kap. 4b) ----------
def motor1(geschwindigkeit):
    # Motor 1 = rechts
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
    # Motor 2 = links (Kopie von motor1, wie in der Lab-Aufgabe aus Kap. 4b)
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


# ---------- Ultraschall (wie in Kap. 4a) ----------
trig = Pin(TRIG, Pin.OUT)
echo = Pin(ECHO, Pin.IN)
trig.value(0)


def messen():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400    # kein Echo
    return laufzeit * 0.0343 / 2


# ---------- Klasse Median (Lab-Aufgabe Kap. 4d, wie Glaetter) ----------
class Median:

    def __init__(self, n):
        self.n = n
        self.werte = []

    def neu(self, wert):
        self.werte.append(wert)
        if len(self.werte) > self.n:
            self.werte.pop(0)
        sortiert = sorted(self.werte)
        return sortiert[len(sortiert) // 2]


# ---------- Klasse Differenzierer (Kap. 4d) ----------
class Differenzierer:

    def __init__(self, dt):
        self.dt = dt
        self.vorher = None

    def neu(self, wert):
        if self.vorher is None:     # erster Wert
            self.vorher = wert
            return 0
        differenz = wert - self.vorher
        self.vorher = wert
        return differenz / self.dt


# ---------- Stossschalter (Entprellen nach Kap. 4c, aber strenger) ----------
taster = Pin(TASTER, Pin.IN, Pin.PULL_UP)
taster_zaehler = 0        # wie viele Takte hintereinander er schon gedrueckt ist


def istTasteGedrueckt():
    # Die alte Version hat nach dem Warten nicht nochmal gelesen.
    # Ein einziges kurzes Zucken beim Fahren hat deshalb schon gereicht.
    # Jetzt: in diesem Takt TASTER_LESEN mal lesen, alle muessen "gedrueckt" sein,
    # und das in TASTER_TAKTE Takten hintereinander.
    global taster_zaehler
    for i in range(TASTER_LESEN):
        if taster.value() != TASTER_GEDRUECKT:
            taster_zaehler = 0
            return False
        time.sleep_ms(2)
    taster_zaehler = taster_zaehler + 1
    return taster_zaehler >= TASTER_TAKTE


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


# ---------- Geradeaus fahren mit Encoder-Korrektur ----------
def geradeaus(g, richtung=1):
    # g ist immer positiv, richtung = 1 vorwaerts, -1 rueckwaerts.
    # Hat das linke Rad insgesamt mehr Impulse gemacht, ist es weiter gefahren.
    # Dann wird links etwas langsamer und rechts etwas schneller.
    # Die Encoder zaehlen in beide Richtungen nur hoch, deshalb funktioniert das
    # rueckwaerts genauso, wenn man erst rechnet und dann die Richtung dranhaengt.
    fehler = impulse_links - impulse_rechts
    korrektur = KP * fehler
    korrektur = begrenzen(korrektur, -MAX_KORREKTUR, MAX_KORREKTUR)
    links = (g - korrektur) * richtung
    rechts = (g + korrektur) * richtung
    motoren(links, rechts)
    return korrektur


def gefahren_cm():
    # Mittelwert aus beiden Raedern in cm (Integrieren, Kap. 4d)
    return (impulse_links + impulse_rechts) / 2 * CM_PRO_IMPULS


# ---------- Hauptprogramm ----------
median = Median(3)
diff = Differenzierer(DT)

zustand = "WARTEN"
g = 0                   # aktuelle Geschwindigkeit in %
korrektur = 0
brems_start = 0
wand_zeit = 0           # wann er die Endwand beruehrt hat
strecke_hin = 0         # gefahrene cm auf der Hinfahrt
rest_cm = 0             # Reststrecke auf der Rueckfahrt
stillstand = 0          # Takte ohne neuen Impuls
summe_vorher = 0
start = time.ticks_ms()
takt = time.ticks_ms()

try:
    motoren(0, 0)
    print("main.py gestartet - warte", STARTWARTEN_MS, "ms an der Startwand")

    while zustand != "FERTIG":
        takt = time.ticks_add(takt, ZYKLUS_MS)

        # 1. Abstand messen und Geschwindigkeit zur Wand ausrechnen (Kap. 4d)
        wert = messen()
        d = median.neu(wert)
        v = diff.neu(d)

        # 2. Was tun? Das haengt vom Zustand ab
        if zustand == "WARTEN":
            motoren(0, 0)
            gewartet = time.ticks_diff(time.ticks_ms(), start)
            if gewartet >= STARTWARTEN_MS:
                impulse_links = 0
                impulse_rechts = 0
                g = START
                zustand = "HINFAHREN"
                print("--> HINFAHREN")

        elif zustand == "HINFAHREN":
            # sanft schneller werden bis VMAX
            if g < VMAX:
                g = g + SCHRITT_HOCH
                if g > VMAX:
                    g = VMAX

            # Muessen wir bremsen?
            zu_nah = d < BREMSEN_AB
            restzeit_knapp = False
            # nur plausible Geschwindigkeiten benutzen (Kap. 4d)
            if v < 0 and v > -MAX_GESCHW_CMS:
                restzeit = d / -v
                if restzeit < RESTZEIT_S:
                    restzeit_knapp = True

            if zu_nah or restzeit_knapp:
                zustand = "BREMSEN"
                brems_start = time.ticks_ms()
                print("--> BREMSEN bei", round(d, 1), "cm")

            korrektur = geradeaus(g)

        elif zustand == "BREMSEN":
            # sanft langsamer werden bis Kriechtempo.
            # Hier wird NICHT mehr schneller, auch wenn der Sensor 400 cm liefert.
            if g > KRIECHEN:
                g = g - SCHRITT_RUNTER
                if g < KRIECHEN:
                    g = KRIECHEN
            korrektur = geradeaus(g)

            # Sicherheit: wenn er zu lange kriecht, anhalten
            gekrochen = time.ticks_diff(time.ticks_ms(), brems_start)
            if gekrochen > MAX_KRIECHZEIT_MS:
                motoren(0, 0)
                g = 0
                print("Sicherheitsstopp: Wand nicht gefunden")
                zustand = "FERTIG"

        elif zustand == "AN_DER_WAND":
            motoren(0, 0)
            g = 0
            korrektur = 0
            gestanden = time.ticks_diff(time.ticks_ms(), wand_zeit)
            if gestanden >= PAUSE_AN_WAND_MS:
                impulse_links = 0
                impulse_rechts = 0
                summe_vorher = 0
                stillstand = 0
                g = START
                zustand = "ZURUECK"
                print("--> ZURUECK, Strecke hin:", round(strecke_hin, 1), "cm")

        elif zustand == "ZURUECK":
            # rueckwaerts sanft schneller werden bis VMAX_ZURUECK
            if g < VMAX_ZURUECK:
                g = g + SCHRITT_HOCH
                if g > VMAX_ZURUECK:
                    g = VMAX_ZURUECK
            rest_cm = strecke_hin - gefahren_cm()
            if rest_cm < BREMSEN_AB_ZURUECK:
                zustand = "ZURUECK_BREMSEN"
                brems_start = time.ticks_ms()
                print("--> ZURUECK_BREMSEN, noch", round(rest_cm, 1), "cm")
            korrektur = geradeaus(g, -1)

        elif zustand == "ZURUECK_BREMSEN":
            if g > KRIECHEN:
                g = g - SCHRITT_RUNTER
                if g < KRIECHEN:
                    g = KRIECHEN
            korrektur = geradeaus(g, -1)
            rest_cm = strecke_hin - gefahren_cm()

            # Startwand erreicht? Beim Kriechen kommen dann (fast) keine Impulse mehr.
            summe = impulse_links + impulse_rechts
            if g == KRIECHEN and summe - summe_vorher < MIN_IMPULSE_TAKT:
                stillstand = stillstand + 1
            else:
                stillstand = 0
            summe_vorher = summe

            if stillstand >= STILLSTAND_TAKTE:
                motoren(0, 0)
                g = 0
                zustand = "AM_START"
                print("--> AM_START, Abweichung zur Hinfahrt:", round(-rest_cm, 1), "cm")
            elif -rest_cm > MAX_UEBERFAHREN_CM:
                motoren(0, 0)
                g = 0
                print("Sicherheitsstopp: schon", MAX_UEBERFAHREN_CM, "cm weiter als die Hinfahrt")
                zustand = "FERTIG"
            elif time.ticks_diff(time.ticks_ms(), brems_start) > MAX_KRIECHZEIT_MS:
                motoren(0, 0)
                g = 0
                print("Sicherheitsstopp: Startwand nicht gefunden")
                zustand = "FERTIG"

        elif zustand == "AM_START":
            motoren(0, 0)
            g = 0
            print("Zurueck an der Startwand - fertig")
            zustand = "FERTIG"

        # 3. Stossschalter: beruehrt er die Wand, sofort anhalten
        if zustand == "HINFAHREN" or zustand == "BREMSEN":
            if istTasteGedrueckt():
                motoren(0, 0)
                g = 0
                strecke_hin = gefahren_cm()
                wand_zeit = time.ticks_ms()
                zustand = "AN_DER_WAND"
                print("--> AN_DER_WAND")

        # 4. Ausgabe fuer die Thonny-Shell
        print(zustand, " d:", round(d, 1), "cm  v:", round(v), "cm/s  rest:", round(rest_cm, 1), "cm  g:", g,
              "%  Korrektur:", round(korrektur, 1), "  Impulse L/R:", impulse_links, impulse_rechts,
              "  Taster:", taster.value(), "x", taster_zaehler)

        # 5. auf den naechsten Takt warten (Kap. 4d)
        rest = time.ticks_diff(takt, time.ticks_ms())
        time.sleep_ms(max(0, rest))

finally:
    # wird auch ausgefuehrt, wenn wir in Thonny auf Stopp druecken
    motoren(0, 0)
    print("Programm beendet, Motoren aus")
