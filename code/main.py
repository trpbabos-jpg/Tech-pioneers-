# Wall-Sprint Team Batman, schnell
# Hin zur Wand, Taster beruehren, zurueck zur Startwand
from machine import Pin, PWM, time_pulse_us
import time

# Pins
rechts_a = PWM(Pin(32), freq=20000, duty_u16=0)   # Motor rechts, MDD3A M2A
rechts_b = PWM(Pin(33), freq=20000, duty_u16=0)   # Motor rechts, MDD3A M2B
links_a = PWM(Pin(25), freq=20000, duty_u16=0)    # Motor links, MDD3A M1A
links_b = PWM(Pin(26), freq=20000, duty_u16=0)    # Motor links, MDD3A M1B
trig_vorne = Pin(15, Pin.OUT, value=0)
echo_vorne = Pin(39, Pin.IN)
taster = Pin(27, Pin.IN, Pin.PULL_UP)             # Taster vorne, gedrueckt = 1
enc_links = Pin(13, Pin.IN, Pin.PULL_UP)
enc_rechts = Pin(14, Pin.IN, Pin.PULL_UP)

# Hinfahrt
V_MAX = 75                      # cm/s
A_HIN = 150                     # cm/s2
BREMSEN_HIN = 100               # cm/s2
BREMSPUNKT_HIN = 45             # cm Echo-Abstand, ab hier auf V_WAND bremsen

# Wand
V_WAND = 14                     # cm/s, Kriechtempo an beiden Waenden
PAUSE_AN_WAND = 285             # ms

# Rueckfahrt
A_ZURUECK = 100                 # cm/s2
BREMSEN_ZURUECK = 80            # cm/s2
BREMSPUNKT_ZURUECK = 40         # cm vor dem Start, ab hier auf V_WAND bremsen

# Motoren
ANLAUF = 20                     # %, ab dieser Leistung drehen die Raeder
FAKTOR_LINKS = 1.04             # linker Motor mehr Leistung vorwaerts, faehrt gerade
FAKTOR_LINKS_ZURUECK = 1.075     # linker Motor mehr Leistung rueckwaerts, faehrt gerade
CM_S_BEI_0 = 10                 # cm/s, Tempo bei kleinster Leistung (ANLAUF)
CM_S_PRO_PROZENT = 0.75

# Sonstiges
START_WARTEN = 3                # s, erlaubt 2 bis 10
MIN_ZEIT = 300                  # ms, Taster erst nach dieser Zeit aktiv
MIN_IMPULSE = 20                # Impulse rueckwaerts, bevor Stillstand zaehlt
STEHT_MS = 200                  # ms ohne Encoder-Impuls = Raeder stehen
ENTPRELLZEIT = 30               # ms
TAKT = 40                       # ms Pause pro Regelschleife
MAX_FAHRZEIT = 60000            # ms, danach Notstopp
CM_PRO_IMPULS = 3.1416 * 8.0 / 224   # cm pro Impuls, Rad 8 cm, 224 Impulse pro Umdrehung


def motor(a, b, prozent):
    # einen Motor ansteuern: plus vorwaerts, minus rueckwaerts, 0 aus
    duty = 0
    if prozent != 0:
        p = ANLAUF + abs(prozent) * (100 - ANLAUF) / 100
        if p > 100:
            p = 100
        duty = int(p * 65535 // 100)
    if prozent > 0:
        a.duty_u16(duty)
        b.duty_u16(0)
    else:
        a.duty_u16(0)
        b.duty_u16(duty)


def fahren(links, rechts):
    # beide Motoren ansteuern, links mit Ausgleichsfaktor
    if links >= 0:
        links = links * FAKTOR_LINKS
    else:
        links = links * FAKTOR_LINKS_ZURUECK
    motor(links_b, links_a, links)      # B-Pin ist vorwaerts
    motor(rechts_b, rechts_a, rechts)


def prozent(geschwindigkeit):
    # Tempo in cm/s in Motorleistung in Prozent umrechnen
    if geschwindigkeit <= 0:
        return 0
    p = (geschwindigkeit - CM_S_BEI_0) / CM_S_PRO_PROZENT
    if p < 1:
        p = 1
    return p


def messen():
    # Ultraschall vorne: Abstand in cm, 400 wenn kein Echo
    trig_vorne.value(1)
    time.sleep_us(10)
    trig_vorne.value(0)
    laufzeit = time_pulse_us(echo_vorne, 1, 30000)     # hoechstens 30 ms warten
    if laufzeit < 0:
        return 400              # kein Echo
    return laufzeit * 0.0343 / 2


werte_vorne = []


def abstand_vorne():
    # mittlerer Wert der letzten 3 Messungen, gegen Ausreisser
    werte_vorne.append(messen())
    if len(werte_vorne) > 3:
        werte_vorne.pop(0)
    return sorted(werte_vorne)[len(werte_vorne) // 2]


def istTasteGedrueckt():
    # Taster lesen, mit Entprellen
    if taster.value() != 1:
        return False
    time.sleep_ms(ENTPRELLZEIT)     # Prellen abwarten
    return taster.value() == 1


impulse_links = 0
impulse_rechts = 0


def zaehle_links(pin):
    # Interrupt: Impuls linkes Rad zaehlen
    global impulse_links
    impulse_links = impulse_links + 1


def zaehle_rechts(pin):
    # Interrupt: Impuls rechtes Rad zaehlen
    global impulse_rechts
    impulse_rechts = impulse_rechts + 1


enc_links.irq(trigger=Pin.IRQ_RISING, handler=zaehle_links)
enc_rechts.irq(trigger=Pin.IRQ_RISING, handler=zaehle_rechts)


def encoder_null():
    # beide Zaehler auf 0 setzen
    global impulse_links, impulse_rechts
    impulse_links = 0
    impulse_rechts = 0


def gefahren():
    # gefahrene Strecke in cm, Mittel beider Raeder
    return (impulse_links + impulse_rechts) / 2 * CM_PRO_IMPULS


start = 0                       # Startzeit in ms


def wand_beruehrt():
    # True, wenn der Taster die Wand beruehrt
    if time.ticks_diff(time.ticks_ms(), start) < MIN_ZEIT:
        return False
    return istTasteGedrueckt()


def pruefe_zeit():
    # Notstopp, wenn die Fahrt zu lange dauert
    if time.ticks_diff(time.ticks_ms(), start) > MAX_FAHRZEIT:
        fahren(0, 0)
        while True:
            time.sleep(1)


letzte = 0                      # letzte Summe der Impulse
letzte_bewegung = 0             # ms


def raeder_stehen():
    # True, wenn STEHT_MS lang kein Impuls kam
    global letzte, letzte_bewegung
    jetzt = impulse_links + impulse_rechts
    if jetzt != letzte:
        letzte = jetzt
        letzte_bewegung = time.ticks_ms()
        return False
    return time.ticks_diff(time.ticks_ms(), letzte_bewegung) > STEHT_MS


v = 0                           # Soll-Tempo in cm/s
letzte_zeit = 0                 # Zeit der letzten Tempo-Rechnung in ms


def neues_tempo(v_ziel):
    # Soll-Tempo v Richtung v_ziel aendern, begrenzt durch beschleunigen und bremsen
    global v, letzte_zeit
    jetzt = time.ticks_ms()
    dt = time.ticks_diff(jetzt, letzte_zeit) / 1000
    letzte_zeit = jetzt
    if v_ziel > v:
        v = v + beschleunigen * dt
        if v > v_ziel:
            v = v_ziel
    else:
        v = v - bremsen * dt
        if v < v_ziel:
            v = v_ziel


# Start: an der Startwand warten
time.sleep(START_WARTEN)
start = time.ticks_ms()

# Hinfahren: beschleunigen, vor der Wand bremsen, bis der Taster drueckt
beschleunigen = A_HIN           # Werte fuer die Hinfahrt
bremsen = BREMSEN_HIN
letzte_zeit = start
encoder_null()
while not wand_beruehrt():
    pruefe_zeit()
    if abstand_vorne() > BREMSPUNKT_HIN:
        neues_tempo(V_MAX)
    else:
        neues_tempo(V_WAND)
    p = prozent(v)
    fahren(p, p)
    time.sleep_ms(TAKT)
fahren(0, 0)

# Wand: Strecke merken, kurz warten
strecke = gefahren()            # fuer die Rueckfahrt merken
time.sleep_ms(PAUSE_AN_WAND)

# Zurueck: rueckwaerts, ab BREMSPUNKT_ZURUECK langsam, bis die Raeder an der Startwand stehen
beschleunigen = A_ZURUECK       # Werte fuer die Rueckfahrt
bremsen = BREMSEN_ZURUECK
v = 0
letzte_zeit = time.ticks_ms()
encoder_null()
while True:
    pruefe_zeit()
    rest = strecke - gefahren()     # Restweg bis zum Start
    if rest > BREMSPUNKT_ZURUECK:
        neues_tempo(V_MAX)
    else:
        neues_tempo(V_WAND)
    p = prozent(v)
    fahren(-p, -p)
    time.sleep_ms(TAKT)
    if impulse_links + impulse_rechts > MIN_IMPULSE and raeder_stehen():
        break                   # Startwand erreicht
fahren(0, 0)