# Testprogramme

Kleine Programme für einzelne Bauteile, z. B. `test_led.py`, `test_motor_links.py`, `test_ultraschall_vorne.py`, `test_encoder.py`.
Nicht löschen: Nach jeder Änderung am Aufbau laufen dieselben Tests noch einmal.

## Vorhandene Tests

| Datei | Bauteil | Pins damals |
| --- | --- | --- |
| `2026-10-20_test_motor.py` | Motor 1 am MDD3A, PWM mit Rampe | GPIO32 / GPIO33 |
| `2026-10-20_test_ultraschall_led.py` | HC-SR04 mit Mittelwert aus 5 Messungen, LED unter 30 cm | Trig 26, Echo 25, LED 2 |
| `2026-10-23_test_encoder.py` | Encoder Motor 1, zählt Impulse mit Richtung | A 13, B 14 |

Die Dateien haben noch die Pins vom Tag im Dateinamen. Seit dem Umbau am 29.10. stimmen sie nicht mehr: vor dem Testen die Pins oben im Programm an `elektronik/pinbelegung.md` anpassen.
