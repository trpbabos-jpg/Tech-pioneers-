# Wall-Sprint Team Batman
from machine import Pin, PWM, time_pulse_us
import time

# Pins
m1a = PWM(Pin(33), freq=20000, duty_u16=0)   # Motor rechts
m1b = PWM(Pin(32), freq=20000, duty_u16=0)
m2a = PWM(Pin(26), freq=20000, duty_u16=0)   # Motor links
m2b = PWM(Pin(25), freq=20000, duty_u16=0)
trig_vorne = Pin(14, Pin.OUT, value=0)
echo_vorne = Pin(12, Pin.IN)
trig_links = Pin(2, Pin.OUT, value=0)
echo_links = Pin(4, Pin.IN)
trig_rechts = Pin(21, Pin.OUT, value=0)
echo_rechts = Pin(36, Pin.IN)
taster = Pin(27, Pin.IN, Pin.PULL_UP)        # Taster vorne
enc_links = Pin(13, Pin.IN, Pin.PULL_UP)     # Encoder links
enc_rechts = Pin(39, Pin.IN)                 # Encoder rechts, 10 kOhm

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
SCHRITT_RUNTER_ZURUECK = 5
EXP_START = 0.5
EXP_ANTEIL = 0.15
PAUSE_AN_WAND = 700             # ms
BREMSEN_AB = 40                 # cm
LANGSAM_AB = 15                 # cm
BREMSEN_AB_ZURUECK = 70         # cm
MIN_ZEIT = 300                  # ms
STEHT_MS = 200
GEDRUECKT = 1
ENTPRELLZEIT = 30
CM_PRO_IMPULS = 3.1416 * 8.0 / 224
TAKT = 50                       # ms
MAX_FAHRZEIT = 60000            # ms

# Seitensensoren
SEITEN_LENKEN = False           # Mitte halten
K_MITTE = 1.0                   # % pro cm Versatz
K_DAEMPFUNG = 5                 # % pro cm Aenderung
KORREKTUR_MAX = 4               # %
SEITE_MAX = 40                  # cm
SEITE_WARTEN = 5000             # us


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


def messen(trig, echo, warten):
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, warten)
    if laufzeit < 0:
        return 400              # kein Echo
    return laufzeit * 0.0343 / 2


werte_vorne = []
werte_links = []
werte_rechts = []


def median(werte, wert):
    werte.append(wert)
    if len(werte) > 3:
        werte.pop(0)
    sortiert = sorted(werte)
    return sortiert[len(sortiert) // 2]


def abstand_vorne():
    return median(werte_vorne, messen(trig_vorne, echo_vorne, 30000))


abstand_l = 400
abstand_r = 400
versatz = 0
aenderung = 0
seiten_ok = False


def seiten_messen():
    global abstand_l, abstand_r, versatz, aenderung, seiten_ok
    abstand_l = median(werte_links, messen(trig_links, echo_links, SEITE_WARTEN))
    abstand_r = median(werte_rechts, messen(trig_rechts, echo_rechts, SEITE_WARTEN))
    vorher_ok = seiten_ok
    seiten_ok = abstand_l < SEITE_MAX and abstand_r < SEITE_MAX
    if seiten_ok:
        neu = (abstand_l - abstand_r) / 2
        aenderung = 0
        if vorher_ok:
            aenderung = neu - versatz
        versatz = neu


def lenken(tempo):
    korrektur = 0
    if SEITEN_LENKEN and seiten_ok:
        korrektur = K_MITTE * versatz + K_DAEMPFUNG * aenderung
        grenze = KORREKTUR_MAX
        if grenze > tempo / 2:
            grenze = tempo / 2
        if korrektur > grenze:
            korrektur = grenze
        if korrektur < -grenze:
            korrektur = -grenze
    return korrektur


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
        print(text, round(abstand, 1), "cm", round(tempo, 1), "% L:", impulse_links, "R:", impulse_rechts,
              "| links:", round(abstand_l, 1), "rechts:", round(abstand_r, 1), "versatz:", round(versatz, 1))


# Start
fahren(0, 0)
i = 0
while i < 3:
    seiten_messen()
    print("Echo vorne:", round(messen(trig_vorne, echo_vorne, 30000), 1),
          "links:", round(abstand_l, 1), "rechts:", round(abstand_r, 1))
    time.sleep_ms(100)
    i = i + 1
print("Seiten lenken:", SEITEN_LENKEN)
time.sleep(3)
start = time.ticks_ms()

# Hinfahren
encoder_null()
tempo = 0
abstand = abstand_vorne()
while abstand > BREMSEN_AB and not wand_beruehrt():
    pruefe_zeit()
    tempo = tempo + SCHRITT_HOCH
    if tempo > VMAX:
        tempo = VMAX
    seiten_messen()
    korrektur = lenken(tempo)
    fahren(tempo - korrektur, tempo + korrektur)
    ausgabe("HIN", abstand, tempo)
    time.sleep_ms(TAKT)
    abstand = abstand_vorne()

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
    seiten_messen()
    korrektur = lenken(tempo)
    fahren(tempo - korrektur, tempo + korrektur)
    ausgabe("BREMS", abstand, tempo)
    time.sleep_ms(TAKT)
    abstand = abstand_vorne()
fahren(0, 0)

# Wand
print("Wand, Abstand:", round(abstand, 1), "Tempo:", round(tempo, 1))
zeit_hin = time.ticks_diff(time.ticks_ms(), start) / 1000
strecke = gefahren()
print("Zeit hin:", zeit_hin, "Strecke:", round(strecke, 1))
print("diff hin:", impulse_links - impulse_rechts, "versatz:", round(versatz, 1))
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
    seiten_messen()
    korrektur = lenken(tempo)
    fahren(-(tempo - korrektur), -(tempo + korrektur))
    ausgabe("ZURUECK", rest, tempo)
    time.sleep_ms(TAKT)
    if impulse_links + impulse_rechts > 20 and raeder_stehen():
        break                   # schon an der Startwand

# Startwand
while True:
    pruefe_zeit()
    fahren(-KRIECHEN, -KRIECHEN)
    time.sleep_ms(TAKT)
    if raeder_stehen():
        print("Startwand erreicht")
        break
fahren(0, 0)
print("versatz Ende:", round(versatz, 1))
print("Fertig nach s:", time.ticks_diff(time.ticks_ms(), start) / 1000)
