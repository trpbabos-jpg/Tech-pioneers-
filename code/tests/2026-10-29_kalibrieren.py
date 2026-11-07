# kalibrieren.py - ANLAUF und Vmax bestimmen (Lab-Aufgabe Kap. 4d)
# Team Batman
#
# TEIL 1: ANLAUF (in der Luft)
#   Die Geschwindigkeit steigt in 2er-Schritten. Sobald ein Rad wirklich dreht
#   (Encoder zaehlt Impulse), ist das die Anlaufschwelle.
# TEIL 2: VMAX (nur auf dem Boden, deshalb erstmal AUS: TEIL2_VMAX = False)
#   Wie in Kap. 4d: Abstand zur Wand messen, 1 s fahren, Abstand wieder messen.
#   Zum Vergleich rechnen wir die Strecke auch aus den Encoder-Impulsen aus.
#
# ANSCHLUSS: Motoren, Encoder und Ultraschall wie im Steckplan
#   Motor 1 (rechts): GPIO14 -> M1A, GPIO27 -> M1B
#
# SO TESTET IHR:
#   1. Vorher motor_test.py: beide Raeder muessen vorwaerts drehen.
#   2. OHNE Ball! Roboter hochheben oder aufbocken, die Raeder muessen frei drehen.
#   3. USB an, Programm starten, Wippschalter an.
#   4. Teil 1 laeuft von selbst und zeigt, ab wie viel % jedes Rad dreht.
#   5. Die Werte als ANLAUF_LINKS und ANLAUF_RECHTS in motor_test.py,
#      drehzahl_test.py, main.py und bremsen_test.py eintragen.
#   6. Teil 2 erst spaeter auf dem Boden: TEIL2_VMAX = True setzen, dann habt ihr
#      10 s Zeit, den Roboter mit ca. 150 cm Abstand vor eine Wand zu stellen.

from machine import Pin, PWM, time_pulse_us
import time

# ---------- Pins (aus unserem Steckplan) ----------
M2B, M2A = 32, 33         # Motor 2, links
M1B, M1A = 27, 14         # Motor 1, rechts
ENC2_A, ENC2_B = 25, 26   # Encoder Motor 2, links
ENC1_A, ENC1_B = 13, 4    # Encoder Motor 1, rechts
TRIG = 19
ECHO = 35

# Motoren als Allererstes auf 0
m1a = PWM(Pin(M1A), freq=20000, duty_u16=0)
m1b = PWM(Pin(M1B), freq=20000, duty_u16=0)
m2a = PWM(Pin(M2A), freq=20000, duty_u16=0)
m2b = PWM(Pin(M2B), freq=20000, duty_u16=0)

# ---------- Einstellungen ----------
RICHTUNG_LINKS = 1            # aus motor_test.py uebernehmen
RICHTUNG_RECHTS = -1          # aus motor_test.py uebernehmen (Kabel: M1A an 14, M1B an 27)
TEIL2_VMAX = False            # Teil 2 nur auf dem Boden vor einer Wand, in der Luft AUS
IMPULSE_PRO_UMDREHUNG = 224   # Kap. 4b, Folie 23
RAD_DURCHMESSER = 8.0         # in cm
MIN_IMPULSE = 20              # ab so vielen Impulsen in 0,5 s dreht das Rad wirklich
VMAX_TEST = 100               # mit dieser Geschwindigkeit wird Vmax gemessen
MIN_ABSTAND_TEST = 120        # so viel Platz (cm) braucht Teil 2 mindestens


def begrenzen(x, unten, oben):
    # aus Kap. 4d
    return max(unten, min(oben, x))


def motor1(geschwindigkeit):
    # Motor 1 = rechts (wie motor() aus Kap. 4b)
    geschwindigkeit = begrenzen(geschwindigkeit, -100, 100)
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
    # Motor 2 = links
    geschwindigkeit = begrenzen(geschwindigkeit, -100, 100)
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


# ---------- Ultraschall (Kap. 4a) ----------
trig = Pin(TRIG, Pin.OUT)
echo = Pin(ECHO, Pin.IN)
trig.value(0)


def messen():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    laufzeit = time_pulse_us(echo, 1, 30000)
    if laufzeit < 0:
        return 400   # kein Echo
    return laufzeit * 0.0343 / 2


def abstand_genau():
    # 5 Messungen, davon der Median (Kap. 4d)
    werte = []
    for i in range(5):
        werte.append(messen())
        time.sleep_ms(60)
    werte.sort()
    return werte[2]


# ---------- Encoder (Fortgeschrittene Kap. 4c) ----------
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


try:
    print("Kalibrieren startet in 3 Sekunden - OHNE Ball, Raeder frei?")
    time.sleep(3)

    # ===== TEIL 1: ANLAUF =====
    print()
    print("TEIL 1: Anlaufschwelle")
    anlauf_links = 0      # 0 heisst: noch nicht gefunden
    anlauf_rechts = 0
    prozent = 0

    while prozent < 60 and (anlauf_links == 0 or anlauf_rechts == 0):
        prozent = prozent + 2
        motoren(prozent, prozent)
        impulse_links = 0
        impulse_rechts = 0
        time.sleep_ms(500)
        print("  ", prozent, "%  Impulse links:", impulse_links, " rechts:", impulse_rechts)

        if anlauf_links == 0 and impulse_links > MIN_IMPULSE:
            anlauf_links = prozent
            print("   -> links dreht ab", prozent, "%")
        if anlauf_rechts == 0 and impulse_rechts > MIN_IMPULSE:
            anlauf_rechts = prozent
            print("   -> rechts dreht ab", prozent, "%")

    motoren(0, 0)
    print("Ergebnis: links ab", anlauf_links, "%, rechts ab", anlauf_rechts, "%")
    print("Eintragen: ANLAUF_LINKS =", anlauf_links, " ANLAUF_RECHTS =", anlauf_rechts)

    # ===== TEIL 2: VMAX =====
    if not TEIL2_VMAX:
        print()
        print("TEIL 2 (Vmax) uebersprungen, laeuft nur auf dem Boden (TEIL2_VMAX = True)")
    else:
        print()
        print("TEIL 2: Vmax - Roboter jetzt ca. 150 cm vor eine Wand stellen!")
        for sekunde in range(10, 0, -1):
            print("  noch", sekunde, "s")
            time.sleep(1)
        d_vorher = abstand_genau()
        print("Abstand vorher:", round(d_vorher, 1), "cm")

    if not TEIL2_VMAX:
        pass
    elif d_vorher < MIN_ABSTAND_TEST:
        print("Zu nah an der Wand! Mindestens", MIN_ABSTAND_TEST, "cm. Abbruch.")
    else:
        impulse_links = 0
        impulse_rechts = 0
        motoren(VMAX_TEST, VMAX_TEST)
        time.sleep(1)
        motoren(0, 0)
        l = impulse_links
        r = impulse_rechts
        time.sleep(1)     # ausrollen lassen

        d_nachher = abstand_genau()
        strecke_us = d_vorher - d_nachher
        print("Abstand nachher:", round(d_nachher, 1), "cm")
        print("Strecke laut Ultraschall:", round(strecke_us, 1), "cm (mit Ausrollen)")

        # Strecke aus den Encodern (Integrieren, Kap. 4d)
        umfang = 3.1416 * RAD_DURCHMESSER
        strecke_links = l / IMPULSE_PRO_UMDREHUNG * umfang
        strecke_rechts = r / IMPULSE_PRO_UMDREHUNG * umfang
        print("Strecke laut Encoder in der 1 s: links", round(strecke_links, 1),
              "cm, rechts", round(strecke_rechts, 1), "cm")
        print("Vmax bei", VMAX_TEST, "% ca.", round((strecke_links + strecke_rechts) / 2, 1), "cm/s")

    print()
    print("Kalibrieren fertig")
finally:
    motoren(0, 0)
    print("Programm beendet, Motoren aus")
