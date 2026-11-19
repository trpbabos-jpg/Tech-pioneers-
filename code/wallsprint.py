# Wall-Sprint Team Batman
from machine import Pin, PWM, time_pulse_us
import time

# Pins
m1a = PWM(Pin(21), freq=20000, duty_u16=0)   # Motor rechts
m1b = PWM(Pin(27), freq=20000, duty_u16=0)
m2a = PWM(Pin(33), freq=20000, duty_u16=0)   # Motor links
m2b = PWM(Pin(32), freq=20000, duty_u16=0)
trig = Pin(19, Pin.OUT, value=0)
echo = Pin(35, Pin.IN)
taster = Pin(22, Pin.IN, Pin.PULL_UP)        # Taster vorne
enc_links = Pin(25, Pin.IN, Pin.PULL_UP)     # Encoder links
enc_rechts = Pin(13, Pin.IN, Pin.PULL_UP)    # Encoder rechts

# Werte
DREHEN_LINKS = 1                # Drehrichtung
DREHEN_RECHTS = 1
ANLAUF = 20
FAKTOR_LINKS = 1.04             # Ausgleich links
FAKTOR_LINKS_ZURUECK = 1.07
VMAX = 70
KRIECHEN = 15
SCHRITT_HOCH = 5
SCHRITT_RUNTER = 6
SCHRITT_HOCH_ZURUECK = 6
SCHRITT_RUNTER_ZURUECK = 8
EXP_START = 0.5
EXP_ANTEIL = 0.15
PAUSE_AN_WAND = 700             # ms
BREMSEN_AB = 40                 # cm
LANGSAM_AB = 15                 # cm
BREMSEN_AB_ZURUECK = 40         # cm
EXTRA_ZURUECK = 15              # cm
MIN_ZEIT = 300                  # ms
STEHT_MS = 200
GEDRUECKT = 1
ENTPRELLZEIT = 30
EINZELN_STOPPEN = True
CM_PRO_IMPULS = 3.1416 * 8.0 / 224
ZURUECK_ANTEIL = 1.3
BREMSEN_ZURUECK_S = 1.3
SUCHEN_S = 1.5
TAKT = 50                       # ms
MAX_FAHRZEIT = 60000            # ms


def motor(a, b, prozent):
    if prozent > 0:
        prozent = ANLAUF + prozent * (100 - ANLAUF) / 100
        a.duty_u16(int(prozent * 65535 // 100))
        b.duty_u16(0)
    elif prozent < 0:
        prozent = ANLAUF - prozent * (100 - ANLAUF) / 100
        a.duty_u16(0)
        b.duty_u16(int(prozent * 65535 // 100))
    else:
        a.duty_u16(0)
        b.duty_u16(0)


def fahren(links, rechts):
    if links >= 0:
        links = links * FAKTOR_LINKS
    else:
        links = links * FAKTOR_LINKS_ZURUECK
    motor(m2a, m2b, DREHEN_LINKS * links)
    motor(m1a, m1b, DREHEN_RECHTS * rechts)


def messen():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400              # kein Echo
    return laufzeit * 0.0343 / 2


werte = []


def median(wert):
    werte.append(wert)
    if len(werte) > 3:
        werte.pop(0)
    sortiert = sorted(werte)
    return sortiert[len(sortiert) // 2]


def istTasteGedrueckt():
    jetzt = taster.value()
    if jetzt != GEDRUECKT:
        return False
    time.sleep_ms(ENTPRELLZEIT)     # Prellen abwarten
    jetzt = taster.value()
    if jetzt == GEDRUECKT:
        return True
    return False


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


def gefahren():
    return (impulse_links + impulse_rechts) / 2 * CM_PRO_IMPULS


start = 0
beruehrt = False


def wand_beruehrt():
    global beruehrt
    if beruehrt:
        return True
    if time.ticks_diff(time.ticks_ms(), start) < MIN_ZEIT:
        return False
    beruehrt = istTasteGedrueckt()
    return beruehrt


def pruefe_zeit():
    if time.ticks_diff(time.ticks_ms(), start) > MAX_FAHRZEIT:
        fahren(0, 0)
        print("Abbruch: zu lange")
        while True:
            time.sleep(1)


takt = 0


def ausgabe(text, abstand, tempo):
    global takt
    takt = takt + 1
    if takt == 4:
        takt = 0
        print(text, round(abstand, 1), "cm", round(tempo, 1), "% L:", impulse_links, "R:", impulse_rechts)


# Start
fahren(0, 0)
if istTasteGedrueckt():
    print("FEHLER: Taster schon gedrueckt")
    while True:
        time.sleep(1)
i = 0
while i < 3:
    print("Echo:", round(messen(), 1))
    time.sleep_ms(100)
    i = i + 1
time.sleep(3)
start = time.ticks_ms()

# Hinfahren
encoder_null()
tempo = 0
abstand = median(messen())
while abstand > BREMSEN_AB and not wand_beruehrt():
    pruefe_zeit()
    tempo = tempo + SCHRITT_HOCH
    if tempo > VMAX:
        tempo = VMAX
    fahren(tempo, tempo)
    ausgabe("HIN", abstand, tempo)
    time.sleep_ms(TAKT)
    abstand = median(messen())
gebremst = not beruehrt

# Bremsen
while not wand_beruehrt():
    pruefe_zeit()
    if abstand > LANGSAM_AB:
        anteil = (abstand - LANGSAM_AB) / (BREMSEN_AB - LANGSAM_AB)
        if anteil > 1:
            anteil = 1
        soll = KRIECHEN + (VMAX - KRIECHEN) * anteil
    else:
        soll = KRIECHEN
    if soll < tempo - SCHRITT_RUNTER:
        tempo = tempo - SCHRITT_RUNTER
    elif soll < tempo:
        tempo = soll
    fahren(tempo, tempo)
    ausgabe("BREMS", abstand, tempo)
    time.sleep_ms(TAKT)
    abstand = median(messen())
fahren(0, 0)

# Wand
print("Wand, Abstand:", round(abstand, 1), "Tempo:", round(tempo, 1))
if not gebremst:
    print("FEHLER: nicht gebremst")
if tempo > KRIECHEN + 1:
    print("FEHLER: nicht im Kriechtempo")
if abstand > LANGSAM_AB:
    print("FEHLER: nicht kurz vor der Wand")
zeit_hin = time.ticks_diff(time.ticks_ms(), start) / 1000
strecke = gefahren()
ziel_links = impulse_links
ziel_rechts = impulse_rechts
print("Zeit hin:", zeit_hin, "Strecke:", round(strecke, 1))
print("diff hin:", impulse_links - impulse_rechts)
encoder_ok = strecke > 20
if not encoder_ok:
    print("Encoder zaehlen nicht")
time.sleep_ms(PAUSE_AN_WAND)

# Zurueck
encoder_null()
t_zurueck = time.ticks_ms()
dauer = zeit_hin * ZURUECK_ANTEIL
tempo = 0
while True:
    pruefe_zeit()
    if encoder_ok:
        rest_l = ziel_links - impulse_links
        rest_r = ziel_rechts - impulse_rechts
        if EINZELN_STOPPEN:
            if rest_l <= 0 and rest_r <= 0:
                break
            rest = rest_l
            if rest_r > rest:
                rest = rest_r
            rest = rest * CM_PRO_IMPULS
        else:
            rest = (rest_l + rest_r) / 2 * CM_PRO_IMPULS
            if rest <= 0:
                break
            rest_l = 1
            rest_r = 1
        anteil = rest / BREMSEN_AB_ZURUECK
        if anteil > 1:
            anteil = 1
        soll = KRIECHEN + (VMAX - KRIECHEN) * anteil
    else:
        rest_s = dauer - time.ticks_diff(time.ticks_ms(), t_zurueck) / 1000
        if rest_s <= 0:
            break
        rest = 0
        rest_l = 1
        rest_r = 1
        if rest_s < BREMSEN_ZURUECK_S:
            soll = KRIECHEN
        else:
            soll = VMAX
    schritt = EXP_START + tempo * EXP_ANTEIL
    if schritt > SCHRITT_HOCH_ZURUECK:
        schritt = SCHRITT_HOCH_ZURUECK
    if soll > tempo + schritt:
        tempo = tempo + schritt
    elif soll < tempo - SCHRITT_RUNTER_ZURUECK:
        tempo = tempo - SCHRITT_RUNTER_ZURUECK
    else:
        tempo = soll
    links = tempo
    rechts = tempo
    if rest_l <= 0:
        links = 0               # links fertig
    if rest_r <= 0:
        rechts = 0              # rechts fertig
    fahren(-links, -rechts)
    ausgabe("ZURUECK", rest, tempo)
    time.sleep_ms(TAKT)
fahren(0, 0)
print("Zurueck L:", impulse_links, "von", ziel_links)
print("Zurueck R:", impulse_rechts, "von", ziel_rechts)

# Startwand
if encoder_ok:
    ende = gefahren() + EXTRA_ZURUECK
    letzte = impulse_links + impulse_rechts
    letzte_bewegung = time.ticks_ms()
    while gefahren() < ende:
        pruefe_zeit()
        fahren(-KRIECHEN, -KRIECHEN)
        time.sleep_ms(TAKT)
        jetzt = impulse_links + impulse_rechts
        if jetzt != letzte:
            letzte = jetzt
            letzte_bewegung = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), letzte_bewegung) > STEHT_MS:
            print("Startwand erreicht")
            break
else:
    fahren(-KRIECHEN, -KRIECHEN)
    time.sleep(SUCHEN_S)
fahren(0, 0)
print("Fertig nach s:", time.ticks_diff(time.ticks_ms(), start) / 1000)
