# Pinbelegung und Verlauf

Board: ESP32-PICO-KIT V1 (Chip ESP32-PICO-V3). Der aktuelle Schaltplan liegt im Miro-Board im Rahmen „Schaltplan“, dazu die Rahmen „Verbindungen“, „Kabel nach Farbe“ und „Bauteile ohne Kabel“:
https://miro.com/app/board/uXjVEZ6PCT0=/?moveToWidget=3458764687840245791

## Stand 29.10.2026 (aktuell auf dem Steckbrett)

Neu verkabelt, damit sich auf dem festen Steckbrett keine Kabel mehr kreuzen.

| Bauteil | Anschluss | ESP32 oder Ziel |
| --- | --- | --- |
| Motor 2 (links), MDD3A | M2A / M2B | GPIO33 / GPIO32 |
| Motor 1 (rechts), MDD3A | M1A / M1B | GPIO14 / GPIO27 |
| MDD3A | GND / 5VO | blaue Schiene / frei |
| Encoder Motor 2 (links) | gelb A / grün B | GPIO25 / GPIO26 |
| Encoder Motor 1 (rechts) | gelb A / grün B | GPIO13 / GPIO4 |
| Beide Encoder | blau + / schwarz GND | 3V3 / blaue Schiene |
| HC-SR04 | Trig | GPIO19 |
| HC-SR04 | Echo | über 1 kΩ an GPIO35, von dort 2,2 kΩ nach GND |
| HC-SR04 | VCC / GND | rote Schiene (5 V) / blaue Schiene |
| Stoßschalter | Kontakt 1 / Kontakt 2 | GPIO22 (Pull-up) / blaue Schiene |
| Schienen | rot / blau | 5V vom ESP32 / GND |
| Akku 4 x AA (ca. 4,8 V) | + / − | über Wippschalter an VB+ / VB− |

Frei bleiben die Startpins 0, 2, 12 und 15. Reserviert für einen zweiten HC-SR04: Trig 21, Echo 34. Die LED ist nicht mehr verbaut.

## Geplant für Grundplatte v2

- Drei HC-SR04 (vorne, links, rechts), weil die Seitenwände aus Blöcken bestehen und nicht gerade sind. Pins für links und rechts noch festlegen und hier eintragen.
- Vom MDD3A-5VO geht ein Kabel zur roten Schiene, damit der ESP32 im Wettbewerb ohne USB vom Akku läuft. Beim Programmieren USB und 5VO nicht gleichzeitig anschließen.
- 5VO liefert laut Cytron-Datenblatt höchstens 200 mA, deshalb bleibt WLAN aus.
- Der Wippschalter ist gleichzeitig Startknopf. Nach dem Booten wartet der Roboter 3 s.

## Frühere Stände

### 23.10.2026: Taster und Encoder dazu

- Taster: GPIO27 über rotes Kabel zum Taster, Taster zur Minus-Schiene, im Code `Pin(27, Pin.IN, Pin.PULL_UP)`. Der Taster ist ein Öffner: gedrückt ergibt 1.
- Encoder Motor 1: gelb GPIO13, grün GPIO14. Encoder Motor 2: gelb GPIO19, grün GPIO4. Blau an 3V3, schwarz an GND.
- Erster Vorschlag für Motor 2 war GPIO18. Den gibt es auf unserem Board nicht, deshalb GPIO4.
- Motortreiber weiter an 21, 22, 32, 33, Ultraschall an 25 und 26, LED an 2.

### 20.10.2026 nachmittags: Motortreiber dazu

- MDD3A: grün GPIO32 zu M1A, rot GPIO33 zu M1B, schwarz GPIO21 zu M2A, weiß GPIO22 zu M2B, orange GND vom MDD3A an die Minus-Schiene (gemeinsame Masse).
- Akku über Schalter an VB+ (rot zum Schalter, gelb zu VB+), schwarz an VB−. Beide Motoren rot und weiß an die Schraubklemmen.
- Sensor bekommt Strom jetzt über die Schienen statt direkt vom ESP32. Grund: übersichtlicher und leichter erweiterbar.
- Regeln: Akku nie ans Steckbrett, 5VO bleibt frei, vor dem Umstecken Schalter aus und USB ab.

### 20.10.2026 vormittags: erster Aufbau

- HC-SR04: Trig an GPIO26, Echo über 1 kΩ an GPIO25, von GPIO25 2,2 kΩ nach GND (macht aus 5 V ca. 3,4 V).
- LED an GPIO2 mit 270 Ω Vorwiderstand, leuchtet unter 30 cm Abstand.
- Fehler beim ersten Aufbau: GPIO2 war nicht mit der LED verbunden, und der 1-kΩ-Widerstand steckte eine Spalte zu weit (an Trig statt an GPIO25). Beides behoben.

## Warum diese Pins und nicht andere

Quelle: Espressif User Guide ESP32-PICO-KIT-1, ESP32-PICO Datenblatt, MicroPython Quick Reference.

- 34 bis 39: können nur lesen und haben keinen internen Pull-up. Für die Encoder brauchen wir den Pull-up.
- 0, 2, 5, 12, 15: Strapping-Pins, ihr Zustand beim Einschalten bestimmt, wie der ESP32 startet. GPIO12 auf high stellt sogar die Flash-Spannung falsch ein.
- 1 und 3: USB-Verbindung zu Thonny.
- 7, 8, 20: laut MicroPython nicht empfohlen bzw. nicht ansprechbar.
- 18 und 23: auf dem ESP32-PICO-V3 nicht angeschlossen.
