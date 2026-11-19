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
MIN_ZEIT = 300                  # ms
STEHT_MS = 200
GEDRUECKT = 1
ENTPRELLZEIT = 30
CM_PRO_IMPULS = 3.1416 * 8.0 / 224
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


letzte = 0
letzte_bewegung = 0


def raeder_stehen():
    global letzte, letzte_bewegung
    jetzt = impulse_links + impulse_rechts
    if jetzt != letzte:
        letzte = jetzt
        letzte_bewegung = time.ticks_ms()
        return False
    if time.ticks_diff(time.ticks_ms(), letzte_bewegung) > STEHT_MS:
        return True
    return False


takt = 0


def ausgabe(text, abstand, tempo):
    global takt
    takt = takt + 1
    if takt == 4:
        takt = 0
        print(text, round(abstand, 1), "cm", round(tempo, 1), "% L:", impulse_links, "R:", impulse_rechts)


# Start
fahren(0, 0)
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
zeit_hin = time.ticks_diff(time.ticks_ms(), start) / 1000
strecke = gefahren()
print("Zeit hin:", zeit_hin, "Strecke:", round(strecke, 1))
print("diff hin:", impulse_links - impulse_rechts)
time.sleep_ms(PAUSE_AN_WAND)

# Zurueck
encoder_null()
tempo = 0
while True:
    pruefe_zeit()
    rest = strecke - gefahren()
    if rest <= 0:
        break
    anteil = rest / BREMSEN_AB_ZURUECK
    if anteil > 1:
        anteil = 1
    soll = KRIECHEN + (VMAX - KRIECHEN) * anteil
    schritt = EXP_START + tempo * EXP_ANTEIL
    if schritt > SCHRITT_HOCH_ZURUECK:
        schritt = SCHRITT_HOCH_ZURUECK
    if soll > tempo + schritt:
        tempo = tempo + schritt
    elif soll < tempo - SCHRITT_RUNTER_ZURUECK:
        tempo = tempo - SCHRITT_RUNTER_ZURUECK
    else:
        tempo = soll
    fahren(-tempo, -tempo)
    ausgabe("ZURUECK", rest, tempo)
    time.sleep_ms(TAKT)
    if impulse_links + impulse_rechts > 20 and raeder_stehen():
        break                   # schon an der Startwand
fahren(0, 0)

# Startwand
while True:
    pruefe_zeit()
    fahren(-KRIECHEN, -KRIECHEN)
    time.sleep_ms(TAKT)
    if raeder_stehen():
        print("Startwand erreicht")
        break
fahren(0, 0)
print("Fertig nach s:", time.ticks_diff(time.ticks_ms(), start) / 1000)
