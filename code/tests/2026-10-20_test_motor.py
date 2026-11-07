# Stand 20.10.2026 (erster Aufbau), alte Pinbelegung, siehe elektronik/pinbelegung.md "Frühere Stände".
# Fuer den aktuellen Aufbau die Pins oben im Programm anpassen.
# motor_test.py
# Motorsteuerung: ESP32 + Motortreiber MDD3A + Getriebemotor FIT0520
# Verdrahtung (wie in den Folien, Kap. 4b):
#   GPIO32 -> MDD3A M1A
#   GPIO33 -> MDD3A M1B
#   GND    -> MDD3A GND   (gemeinsame Masse, ganz wichtig!)
#   Motor rot/weiss -> Klemmen M1A/M1B
#   Akkupack 4 x AA (ca. 4,8 V) -> VB+ / VB-

from machine import Pin, PWM
import time

m1a = PWM(Pin(32), freq=20000, duty_u16=0)   # M1A
m1b = PWM(Pin(33), freq=20000, duty_u16=0)   # M1B


def motor(geschwindigkeit):
    # Werte auf -100 ... 100 begrenzen (sonst wird duty zu gross)
    if geschwindigkeit > 100:
        geschwindigkeit = 100
    if geschwindigkeit < -100:
        geschwindigkeit = -100

    duty = abs(geschwindigkeit) * 65535 // 100
    if geschwindigkeit > 0:
        richtung = "vorwärts"
        m1a.duty_u16(duty)
        m1b.duty_u16(0)
    elif geschwindigkeit < 0:
        richtung = "rückwärts"
        m1a.duty_u16(0)
        m1b.duty_u16(duty)
    else:
        richtung = "Stopp"
        m1a.duty_u16(0)
        m1b.duty_u16(0)
    print("Motor:", geschwindigkeit, "% ->", richtung, " duty:", duty)


def rampe(von, bis, schritt):
    # sanft von "von" nach "bis" fahren, in Schritten von "schritt"
    g = von
    while g != bis:
        motor(g)
        time.sleep_ms(300)
        g = g + schritt
    motor(bis)


# Fahrprogramm als Endlosschleife
try:
    while True:
        print("--- vorwärts ---")
        rampe(0, 100, 20)       # anfahren
        time.sleep(2)
        rampe(100, 0, -20)      # abbremsen
        time.sleep(1)

        print("--- rückwärts ---")
        rampe(0, -100, -20)     # anfahren
        time.sleep(2)
        rampe(-100, 0, 20)      # abbremsen
        time.sleep(1)
finally:
    # Wird auch ausgeführt, wenn du in Thonny auf Stopp drückst:
    # so bleibt der Motor nicht einfach weiterlaufen.
    motor(0)
    print("Programm beendet, Motor aus")
