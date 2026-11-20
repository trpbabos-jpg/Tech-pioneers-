# Simulation: Ball in der Schale (20.11.2026)

Mit einer Simulation wurden die Fahrwerte für `code/wallsprint_schnell.py` (Wall-Sprint) und `code/wallsprint_abnahme.py` (Abnahme) gesucht. Die Simulation ersetzt keinen Test mit dem echten Roboter.

## Annahmen

| Größe | Wert | Quelle |
| --- | --- | --- |
| Schale | Ø 102 mm am Rand, 12,3 mm hoch, kugelförmig gewölbt | Excel / `cad/grundplatte-v2-entscheidungen.md`, Höhe noch nicht nachgemessen |
| Ball | Ø 40 mm, rollt ohne zu rutschen | Regeln |
| Geschwindigkeit | ca. 10 cm/s + 0,75 cm/s pro % (15 % = 21 cm/s, 100 % = 84,5 cm/s) | `doku/messwerte.md`, 29.10. |
| Motor-Trägheit | 0,12 s, zum Vergleich 0,25 s | geschätzt |

## Grenzen aus der Schale

- Rand bei ca. 27° (gemessen vom tiefsten Punkt)
- gleichmäßige Beschleunigung: Ball bleibt bis ca. 5 m/s² drin
- Stoß gegen die Wand: Ball fliegt ab ca. 0,58 m/s Geschwindigkeitsänderung raus
- Ball pendelt mit ca. 0,7 s pro Hin und Her

## Ergebnis

| Version | Fahrzeit | Ball pendelt bis | Stoß Endwand / Startwand |
| --- | --- | --- | --- |
| alter Code (wallsprint.py) | 8,4 s | 18° | 33 / 24 cm/s |
| schnell (Motoren 0,12 s) | 7,2 s | 12° | 12 / 13 cm/s |
| schnell (Motoren 0,25 s) | 7,0 s | 16° | 26 / 25 cm/s |
| Abnahme (ganzer Durchgang, langsam) | 13,4 s | 6 bis 7,5° | 11 bis 13 / 11 bis 13 cm/s |

Werte schnell: V_MAX 75 cm/s, A_HOCH 150 cm/s², A_BREMSEN 100 cm/s², RUCK 800 cm/s³, VORHALT 0,3 s, STOPP_ABSTAND 11 cm, V_WAND 12 cm/s.
Werte Abnahme: V_MAX 40 cm/s, A_HOCH 30 cm/s², A_BREMSEN 25 cm/s², RUCK 80 cm/s³, STOPP_ABSTAND 14 cm, V_WAND 10 cm/s, Pause an der Wand 1 s. Seitlich höchstens 4 cm, auch bei 4 % Unterschied zwischen den Rädern.

V_MAX bleibt bei 75 cm/s, damit der linke Motor (FAKTOR_LINKS 1,04) noch Luft zum Gegenlenken hat.
