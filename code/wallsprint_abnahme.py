# Abnahme Team Batman, sicher
from machine import Pin, PWM, time_pulse_us
import time

# Pins
rechts_a = PWM(Pin(32), freq=20000, duty_u16=0)   # Motor rechts, MDD3A M2A
rechts_b = PWM(Pin(33), freq=20000, duty_u16=0)   # MDD3A M2B
links_a = PWM(Pin(25), freq=20000, duty_u16=0)    # Motor links, MDD3A M1A
links_b = PWM(Pin(26), freq=20000, duty_u16=0)    # MDD3A M1B
trig_vorne = Pin(15, Pin.OUT, value=0)
echo_vorne = Pin(39, Pin.IN)
trig_links = Pin(2, Pin.OUT, value=0)
echo_links = Pin(34, Pin.IN)
trig_rechts = Pin(21, Pin.OUT, value=0)
echo_rechts = Pin(36, Pin.IN)
taster = Pin(27, Pin.IN, Pin.PULL_UP)        # Taster vorne
enc_links = Pin(13, Pin.IN, Pin.PULL_UP)     # Encoder links
enc_rechts = Pin(14, Pin.IN, Pin.PULL_UP)    # Encoder rechts

# Fahren
V_MAX = 40                      # cm/s
V_WAND = 10                     # cm/s, an der Wand
A_HOCH = 30                     # cm/s2
A_BREMSEN = 25                  # cm/s2
RUCK = 80                       # cm/s3
RUCK_ZURUECK = 80               # cm/s3
STOPP_ABSTAND = 14              # cm Echo
VORHALT = 0.3                   # s
PAUSE_AN_WAND = 1000            # ms

# Motoren
DREHEN_LINKS = -1               # Drehrichtung
DREHEN_RECHTS = -1
ANLAUF = 20
FAKTOR_LINKS = 1.04             # Ausgleich links
FAKTOR_LINKS_ZURUECK = 1.07
CM_S_BEI_0 = 10                 # cm/s
CM_S_PRO_PROZENT = 0.75

# Seitensensoren
SEITEN_LENKEN = True            # Mitte halten
K_MITTE = 1.0                   # % pro cm Versatz
K_DAEMPFUNG = 5                 # % pro cm Aenderung
KORREKTUR_MAX = 4               # %
SEITE_MAX = 40                  # cm

# Sonstiges
MIN_ZEIT = 300                  # ms
STEHT_MS = 200                  # ms
ENTPRELLZEIT = 30               # ms
CM_PRO_IMPULS = 3.1416 * 8.0 / 224
TAKT = 40                       # ms
MAX_FAHRZEIT = 60000            # ms


def motor(a, b, prozent):
    if prozent > 0:
        prozent = ANLAUF + prozent * (100 - ANLAUF) / 100
        if prozent > 100:
            prozent = 100
        a.duty_u16(int(prozent * 65535 // 100))
        b.duty_u16(0)
    elif prozent < 0:
        prozent = ANLAUF - prozent * (100 - ANLAUF) / 100
        if prozent > 100:
            prozent = 100
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
    motor(links_a, links_b, DREHEN_LINKS * links)
    motor(rechts_a, rechts_b, DREHEN_RECHTS * rechts)


def prozent(geschwindigkeit):
    if geschwindigkeit <= 0:
        return 0
    p = (geschwindigkeit - CM_S_BEI_0) / CM_S_PRO_PROZENT
    if p < 1:
        p = 1
    return p


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
    abstand_l = median(werte_links, messen(trig_links, echo_links, 5000))
    abstand_r = median(werte_rechts, messen(trig_rechts, echo_rechts, 5000))
    vorher_ok = seiten_ok
    seiten_ok = abstand_l < SEITE_MAX and abstand_r < SEITE_MAX
    if seiten_ok:
        neu = (abstand_l - abstand_r) / 2
        aenderung = 0
        if vorher_ok:
            aenderung = neu - versatz
        versatz = neu


def lenken(p):
    korrektur = 0
    if SEITEN_LENKEN and seiten_ok:
        korrektur = K_MITTE * versatz + K_DAEMPFUNG * aenderung
        grenze = KORREKTUR_MAX
        if grenze > p / 2:
            grenze = p / 2
        if korrektur > grenze:
            korrektur = grenze
        if korrektur < -grenze:
            korrektur = -grenze
    return korrektur


def istTasteGedrueckt():
    jetzt = taster.value()
    if jetzt != 1:
        return False
    time.sleep_ms(ENTPRELLZEIT)     # Prellen abwarten
    jetzt = taster.value()
    if jetzt == 1:
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


v = 0
a = 0
ruck = RUCK
letzte_zeit = 0
v_ist = 0
mess_impulse = 0
mess_zeit = 0


def ist_messen():
    # echte Geschwindigkeit aus den Encodern
    global v_ist, mess_impulse, mess_zeit
    jetzt = time.ticks_ms()
    dt = time.ticks_diff(jetzt, mess_zeit)
    if dt >= 100:
        summe = impulse_links + impulse_rechts
        v_ist = (summe - mess_impulse) / 2 * CM_PRO_IMPULS / dt * 1000
        mess_impulse = summe
        mess_zeit = jetzt


def neues_tempo(v_ziel):
    # sanft schneller (Ruck begrenzt), bremsen hoechstens A_BREMSEN
    global v, a, letzte_zeit
    jetzt = time.ticks_ms()
    dt = time.ticks_diff(jetzt, letzte_zeit) / 1000
    letzte_zeit = jetzt
    if dt > 0.2:
        dt = 0.2
    if v_ziel > V_MAX:
        v_ziel = V_MAX
    if v_ziel > v:
        a = a + ruck * dt
        if a > A_HOCH:
            a = A_HOCH
        v = v + a * dt
        if v > v_ziel:
            v = v_ziel
    else:
        a = 0
        v_neu = v - A_BREMSEN * 1.3 * dt
        if v_ziel > v_neu:
            v_neu = v_ziel
        v = v_neu


def bremsweg_tempo(rest):
    # so schnell, dass er mit A_BREMSEN bis rest auf V_WAND kommt
    if rest <= 0:
        return V_WAND
    return (V_WAND * V_WAND + 2 * A_BREMSEN * rest) ** 0.5


takt = 0


def ausgabe(text, abstand):
    global takt
    takt = takt + 1
    if takt == 4:
        takt = 0
        print(text, round(abstand, 1), "cm soll:", round(v, 1), "ist:", round(v_ist, 1), "cm/s L:", impulse_links,
              "R:", impulse_rechts, "| versatz:", round(versatz, 1))


# Start
fahren(0, 0)
i = 0
while i < 3:
    seiten_messen()
    print("Echo vorne:", round(messen(trig_vorne, echo_vorne, 30000), 1),
          "links:", round(abstand_l, 1), "rechts:", round(abstand_r, 1))
    time.sleep_ms(100)
    i = i + 1
time.sleep(3)
start = time.ticks_ms()
letzte_zeit = start

# Hinfahren
encoder_null()
mess_impulse = 0
mess_zeit = start
abstand = abstand_vorne()
while not wand_beruehrt():
    pruefe_zeit()
    rest = abstand - v * VORHALT - STOPP_ABSTAND
    neues_tempo(bremsweg_tempo(rest))
    seiten_messen()
    p = prozent(v)
    korrektur = lenken(p)
    fahren(p - korrektur, p + korrektur)
    ist_messen()
    ausgabe("HIN", abstand)
    time.sleep_ms(TAKT)
    abstand = abstand_vorne()
fahren(0, 0)

# Wand
print("Wand, Abstand:", round(abstand, 1), "Tempo ist:", round(v_ist, 1))
zeit_hin = time.ticks_diff(time.ticks_ms(), start) / 1000
strecke = gefahren()
print("Zeit hin:", zeit_hin, "Strecke:", round(strecke, 1))
print("diff hin:", impulse_links - impulse_rechts, "versatz:", round(versatz, 1))
time.sleep_ms(PAUSE_AN_WAND)

# Zurueck
encoder_null()
v = 0
a = 0
ruck = RUCK_ZURUECK
letzte_zeit = time.ticks_ms()
mess_impulse = 0
mess_zeit = letzte_zeit
while True:
    pruefe_zeit()
    rest = strecke - gefahren() - v * VORHALT
    if rest <= 0:
        break
    neues_tempo(bremsweg_tempo(rest))
    seiten_messen()
    p = prozent(v)
    korrektur = lenken(p)
    fahren(-(p - korrektur), -(p + korrektur))
    ist_messen()
    ausgabe("ZURUECK", rest)
    time.sleep_ms(TAKT)
    if impulse_links + impulse_rechts > 20 and raeder_stehen():
        break                   # schon an der Startwand

# Startwand
p = prozent(V_WAND)
while True:
    pruefe_zeit()
    fahren(-p, -p)
    time.sleep_ms(TAKT)
    if raeder_stehen():
        print("Startwand erreicht")
        break
fahren(0, 0)
print("versatz Ende:", round(versatz, 1))
print("Fertig nach s:", time.ticks_diff(time.ticks_ms(), start) / 1000)
