# Selbsttest Team Batman
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

# Werte wie im Fahrprogramm
DREHEN_LINKS = -1               # Drehrichtung
DREHEN_RECHTS = -1
ANLAUF = 20
FAKTOR_LINKS = 1.04             # Ausgleich links
FAKTOR_LINKS_ZURUECK = 1.07
ENTPRELLZEIT = 30               # ms

# Test
N = 10                          # Messungen pro Sensor
TEST_TEMPO = 30                 # %
TEST_ZEIT = 1500                # ms
GLEICH_TEMPO = 50               # %
GLEICH_ZEIT = 3000              # ms
MIN_IMPULSE = 50
SCHWANKUNG = 3                  # cm
SEITE_MAX = 40                  # cm


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


def messen(trig, echo):
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400              # kein Echo
    return laufzeit * 0.0343 / 2


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


probleme = 0


def problem(text):
    global probleme
    probleme = probleme + 1
    print("   PROBLEM:", text)


def ok(text):
    print("   OK:", text)


def echo_testen(name, trig, echo, seite):
    werte = []
    ohne = 0
    i = 0
    while i < N:
        wert = messen(trig, echo)
        if wert >= 400:
            ohne = ohne + 1
        else:
            werte.append(wert)
        time.sleep_ms(60)
        i = i + 1
    if len(werte) == 0:
        problem(name + ": kein einziges Echo -> Trig/Echo-Kabel, Teiler 1k/2,2k, VCC/GND pruefen")
        return
    werte = sorted(werte)
    mitte = werte[len(werte) // 2]
    spanne = werte[len(werte) - 1] - werte[0]
    print("  ", name, "Abstand:", round(mitte, 1), "cm, Spanne:", round(spanne, 1), "cm, ohne Echo:", ohne, "von", N)
    if ohne > 0:
        problem(name + ": " + str(ohne) + " Messungen ohne Echo -> Wackelkontakt oder Sensor schraeg")
    if spanne > SCHWANKUNG:
        problem(name + ": Werte schwanken um " + str(round(spanne, 1)) + " cm -> Sensor fest? Stoert ein anderer Sensor?")
    if mitte < 3:
        problem(name + ": unter 3 cm -> Sensor sieht eigenes Teil oder Echo-Pin falsch")
    if seite and mitte > SEITE_MAX:
        problem(name + ": ueber " + str(SEITE_MAX) + " cm -> Bande nicht in Reichweite (nur auf der Bahn wichtig)")
    if ohne == 0 and spanne <= SCHWANKUNG and mitte >= 3:
        ok(name + " misst sauber")


def motor_testen(name, links, rechts):
    encoder_null()
    fahren(links, rechts)
    time.sleep_ms(TEST_ZEIT)
    fahren(0, 0)
    time.sleep_ms(300)
    print("  ", name, "-> Encoder L:", impulse_links, "R:", impulse_rechts)


# Start
fahren(0, 0)
print("===== Selbsttest Team Batman =====")
print("Roboter aufbocken, Raeder frei, Akku an")
time.sleep(3)

# 1. Taster
print("1. Taster")
if taster.value() == 1:
    problem("meldet gedrueckt, obwohl keiner drueckt -> Kabel an GPIO27 / GND, Buegel klemmt?")
else:
    ok("nicht gedrueckt = 0")
print("   jetzt den Taster druecken (10 s Zeit)")
gedrueckt = False
t0 = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), t0) < 10000:
    if taster.value() == 1:
        time.sleep_ms(ENTPRELLZEIT)     # Prellen abwarten
        if taster.value() == 1:
            gedrueckt = True
            break
    time.sleep_ms(10)
if gedrueckt:
    ok("Druck erkannt = 1")
else:
    problem("kein Druck erkannt -> Kabel, Taster, Oeffner/Schliesser?")
time.sleep(1)

# 2. Ultraschall
print("2. Ultraschall (nacheinander)")
echo_testen("vorne", trig_vorne, echo_vorne, False)
echo_testen("links", trig_links, echo_links, True)
echo_testen("rechts", trig_rechts, echo_rechts, True)

# 3. Motoren und Encoder einzeln
print("3. Motoren und Encoder einzeln, je", TEST_ZEIT, "ms mit", TEST_TEMPO, "%")
print("   Schauen: dreht das genannte Rad VORWAERTS?")
time.sleep(2)
motor_testen("nur LINKS vorwaerts", TEST_TEMPO, 0)
l = impulse_links
r = impulse_rechts
if l < MIN_IMPULSE and r >= MIN_IMPULSE:
    problem("links dreht, aber Encoder RECHTS zaehlt -> Encoder-Kabel vertauscht (13/14)")
elif l < MIN_IMPULSE:
    problem("Encoder links zaehlt nicht -> Motor links dreht nicht (25/26, M1A/M1B) oder Encoder gelb an GPIO13 / 3V3 / GND")
else:
    ok("Encoder links zaehlt")
if r >= MIN_IMPULSE and l >= MIN_IMPULSE:
    problem("beim linken Motor zaehlen beide Encoder -> Kabel doppelt oder Stoerung")
print("   -> Rad links falsch herum? Dann DREHEN_LINKS = -1")
time.sleep(1)
motor_testen("nur RECHTS vorwaerts", 0, TEST_TEMPO)
l = impulse_links
r = impulse_rechts
if r < MIN_IMPULSE and l >= MIN_IMPULSE:
    problem("rechts dreht, aber Encoder LINKS zaehlt -> Encoder-Kabel vertauscht (13/14)")
elif r < MIN_IMPULSE:
    problem("Encoder rechts zaehlt nicht -> Motor rechts dreht nicht (32/33, M2A/M2B) oder Encoder gelb an GPIO14 / 3V3 / GND")
else:
    ok("Encoder rechts zaehlt")
if r >= MIN_IMPULSE and l >= MIN_IMPULSE:
    problem("beim rechten Motor zaehlen beide Encoder -> Kabel doppelt oder Stoerung")
print("   -> Rad rechts falsch herum? Dann DREHEN_RECHTS = -1")
time.sleep(1)

# 4. Gleichlauf
print("4. Gleichlauf, beide", GLEICH_TEMPO, "% fuer", GLEICH_ZEIT, "ms")
encoder_null()
fahren(GLEICH_TEMPO, GLEICH_TEMPO)
time.sleep_ms(GLEICH_ZEIT)
fahren(0, 0)
time.sleep_ms(500)
l = impulse_links
r = impulse_rechts
print("   vorwaerts L:", l, "R:", r)
if l > MIN_IMPULSE and r > MIN_IMPULSE:
    neu = FAKTOR_LINKS * r / l
    print("   Vorschlag FAKTOR_LINKS =", round(neu, 3))
    if neu > 1.15 or neu < 0.85:
        problem("Raeder sehr ungleich (mehr als 15 %) -> Rad schleift, Motor oder Encoder pruefen")
    else:
        ok("Unterschied vorwaerts " + str(round((l - r) * 100 / r, 1)) + " %")
encoder_null()
fahren(-GLEICH_TEMPO, -GLEICH_TEMPO)
time.sleep_ms(GLEICH_ZEIT)
fahren(0, 0)
time.sleep_ms(500)
l = impulse_links
r = impulse_rechts
print("   rueckwaerts L:", l, "R:", r)
if l > MIN_IMPULSE and r > MIN_IMPULSE:
    neu = FAKTOR_LINKS_ZURUECK * r / l
    print("   Vorschlag FAKTOR_LINKS_ZURUECK =", round(neu, 3))
    if neu > 1.15 or neu < 0.85:
        problem("Raeder rueckwaerts sehr ungleich (mehr als 15 %)")
    else:
        ok("Unterschied rueckwaerts " + str(round((l - r) * 100 / r, 1)) + " %")
print("   (aufgebockt drehen die Raeder freier als auf dem Boden, Faktor auf der Bahn nachpruefen)")

# Ergebnis
fahren(0, 0)
print("===== Ergebnis =====")
if probleme == 0:
    print("Alles OK")
else:
    print("Probleme:", probleme, "-> oben nach PROBLEM suchen")
