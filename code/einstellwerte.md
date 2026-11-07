# Einstellwerte im Code

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

## Stand 03.11.2026 (`code/main.py`)

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
| `code/main.py` | aktuelles Fahrprogramm: hin, sanft bremsen, Wand mit Stoßschalter berühren, rückwärts über die Encoder zurück | 03.11., noch nicht getestet |
| `code/fahren_v1_zustaende_hin_rueck.py` | erste Version mit Zuständen (WARTEN, HINFAHREN, BREMSEN …), Rückfahrt erkennt die Startwand an stehenden Rädern | 29.10. |
| `code/fahren_v2_vereinfacht.py` | vereinfachte Version in drei Schritten, Median aus 3 Messungen | 30.10. |
| `code/fahren_v3_vmax100.py` | wie v2 mit VMAX 100 und schnelleren Schritten | 03.11. |
| `code/tests/2026-10-29_motor_test.py` | prüft, ob beide Räder vorwärts drehen | 29.10. |
| `code/tests/2026-10-29_kalibrieren.py` | Anlaufschwelle (in der Luft) und Vmax vor der Wand (auf dem Boden, `TEIL2_VMAX = True`) | 29.10. |
| `code/tests/2026-10-29_drehzahl_test.py` | U/min links und rechts bei 15 bis 100 %, daraus der Faktor | 29.10. |
| `code/tests/2026-10-29_bremsen_test.py` | Bremsen vor der Wand ohne Stoßschalter, Ziel 15 cm | 29.10. |

Ältere Bauteiltests (20. und 23.10.) stehen in `code/tests/README.md`. Fehlt noch: `taster_test.py` (bitte aus Thonny hochladen).
