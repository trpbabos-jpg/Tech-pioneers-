# Einstellwerte im Code

## Stand 24.11.2026, Abgabestand (`code/main.py` = `wallsprint_schnell.py`)

Neu geschrieben für die Grundplatte v2 und den Schaltplan v2: Das Tempo wird in cm/s geplant und über Beschleunigung und Bremsverzögerung begrenzt, damit der Ball in der Schale bleibt. Die Werte wurden mit einer Simulation des Balls in der Schale gesucht und am Roboter mit Haube eingestellt.

| Wert | Stand | Bedeutung |
| --- | --- | --- |
| `V_MAX` | 75 cm/s | Höchsttempo hin und zurück |
| `A_HIN` / `BREMSEN_HIN` | 150 / 100 cm/s² | Beschleunigen und Bremsen auf der Hinfahrt |
| `BREMSPUNKT_HIN` | 45 cm | Echo-Abstand, ab dem auf `V_WAND` gebremst wird |
| `V_WAND` | 14 cm/s | Kriechtempo an beiden Wänden |
| `PAUSE_AN_WAND` | 285 ms | Pause nach dem Berühren der Zielwand |
| `A_ZURUECK` / `BREMSEN_ZURUECK` | 100 / 80 cm/s² | Beschleunigen und Bremsen auf der Rückfahrt |
| `BREMSPUNKT_ZURUECK` | 40 cm | Reststrecke vor der Startwand, ab der auf `V_WAND` gebremst wird |
| `ANLAUF` | 20 % | ab dieser Leistung drehen die Räder (kalibrieren.py, 29.10.) |
| `FAKTOR_LINKS` / `FAKTOR_LINKS_ZURUECK` | 1,04 / 1,075 | Ausgleich für den linken Motor vorwärts und rückwärts, mit Haube auf einer geraden Linie eingestellt |
| `CM_S_BEI_0` / `CM_S_PRO_PROZENT` | 10 cm/s / 0,75 cm/s pro % | Umrechnung von Tempo in Motorleistung |
| `START_WARTEN` | 3 s | Wartezeit an der Startwand (Regel: 2 bis 10 s) |
| `MIN_ZEIT` | 300 ms | Stoßschalter erst nach dieser Zeit aktiv |
| `MIN_IMPULSE` / `STEHT_MS` | 20 / 200 ms | Rückfahrt endet, wenn die Räder nach mindestens 20 Impulsen 200 ms stehen (Startwand erreicht) |
| `ENTPRELLZEIT` | 30 ms | Stoßschalter zweimal lesen, dazwischen 30 ms |
| `TAKT` | 40 ms | Länge eines Regeltakts |
| `MAX_FAHRZEIT` | 60 s | danach Notstopp |
| `CM_PRO_IMPULS` | π × 8 cm / 224 | ca. 0,112 cm pro Encoder-Impuls |

Ältere Stände folgen darunter.


Stand 29.10.2026, nach der Neuverkabelung und der neuen Kalibrierung. Wenn ihr einen Wert ändert, hier eine neue Zeile mit Datum dazuschreiben statt die alte zu löschen.

| Wert | Stand | Herkunft |
| --- | --- | --- |
| `RICHTUNG_LINKS` / `RICHTUNG_RECHTS` | 1 / −1 | motor_test.py |
| `ANLAUF_LINKS` / `ANLAUF_RECHTS` | 20 % / 20 % | kalibrieren.py in der Luft, 29.10. |
| `FAKTOR_LINKS` | 0,94 | drehzahl_test.py in der Luft, 29.10. |
| `VMAX` | 50 % | main.py |
| `KRIECHEN` | 15 % | bremsen_test.py auf dem Boden |
| `MAX_GESCHW_CMS` | 120 | Vmax-Messung auf dem Boden |
| `TASTER_TAKTE` | 1 | Fahrtest mit main.py, 29.10. |
| Impulse pro Radumdrehung | 224 | SBC Kap. 4b, Folie 23 |
| Raddurchmesser | 8 cm | Rad 80 mm aus dem Starter Kit |

## Stand 03.11.2026 (`code/main_2026-11-03.py`, damals `main.py`)

Ab der vereinfachten Version (30.10.) gibt es nur noch einen `ANLAUF` für beide Räder und keine `RICHTUNG_`-Werte mehr, der rechte Motor wird in `motoren()` umgedreht.

| Wert | Stand | Herkunft |
| --- | --- | --- |
| `ANLAUF` | 20 % | kalibrieren.py, 29.10. |
| `FAKTOR_LINKS` | 0,7 | auf dem Boden ausprobiert, gleicht die Mechanik aus (gemessen in der Luft: 0,94). Noch nicht mit drehzahl_test.py geprüft |
| `FAKTOR_LINKS_ZURUECK` | 0,7 | Startwert, mit „diff zurueck“ in der Shell einstellen (Schritte 0,05) |
| `VMAX` | 80 % | ausprobiert |
| `KRIECHEN` | 20 % | ausprobiert |
| `SCHRITT_HOCH` / `SCHRITT_RUNTER` | 6 % / 7 % pro Takt | ausprobiert |
| `BREMSEN_AB` | 50 cm | Ultraschall sitzt ca. 10 cm hinter dem Stoßschalter |
| `BREMSEN_AB_ZURUECK` | 45 cm Reststrecke | ausprobiert |
| `KP` | 0,5 | Korrektur höchstens 8 % bei VMAX, wird mit dem Tempo kleiner (`8 * g / VMAX`) |
| `TAKT_MS` | 50 ms | |
| Taster | 7-mal lesen, alle müssen gedrückt sein | Fehlauslösung beim Fahren, 29.10. |

Frühere Stände dazwischen (30.10.: VMAX 70, KRIECHEN 15, BREMSEN_AB 35, Faktor 0,95; 03.11. vormittags: VMAX 100, KRIECHEN 10, Faktor 0,84) stehen in `fahren_v2_vereinfacht.py` und `fahren_v3_vmax100.py`.

## Programme

| Datei | Was | Stand |
| --- | --- | --- |
| `code/main.py`, `code/wallsprint_schnell.py` | Abgabestand: hin mit Tempo-Rampe, ab 45 cm auf Kriechtempo, Wand mit Stoßschalter berühren, rückwärts über die Encoder zurück bis zur Startwand | 24.11. |
| `code/main_2026-11-03.py` | frühere `main.py` mit Geradeausregelung über die Encoder, Pins vom 29.10. | 03.11. |
| `code/fahren_v1_zustaende_hin_rueck.py` | erste Version mit Zuständen (WARTEN, HINFAHREN, BREMSEN …), Rückfahrt erkennt die Startwand an stehenden Rädern | 29.10. |
| `code/fahren_v2_vereinfacht.py` | vereinfachte Version in drei Schritten, Median aus 3 Messungen | 30.10. |
| `code/fahren_v3_vmax100.py` | wie v2 mit VMAX 100 und schnelleren Schritten | 03.11. |
| `code/tests/2026-10-29_motor_test.py` | prüft, ob beide Räder vorwärts drehen | 29.10. |
| `code/tests/2026-10-29_kalibrieren.py` | Anlaufschwelle (in der Luft) und Vmax vor der Wand (auf dem Boden, `TEIL2_VMAX = True`) | 29.10. |
| `code/tests/2026-10-29_drehzahl_test.py` | U/min links und rechts bei 15 bis 100 %, daraus der Faktor | 29.10. |
| `code/tests/2026-10-29_bremsen_test.py` | Bremsen vor der Wand ohne Stoßschalter, Ziel 15 cm | 29.10. |

Ältere Bauteiltests (20. und 23.10.) stehen in `code/tests/README.md`. Die Testprogramme haben die Pins vom 29.10.; vor dem Testen oben im Programm an `elektronik/schaltplan_v2.pdf` anpassen.
