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

## Programme

Diese Programme gibt es bisher. Bitte jeweils den neuesten Stand aus Thonny hier in `code/` bzw. `code/tests/` hochladen:

- `motor_test.py`, `ultraschall_test.py`, `taster_test.py` (Tests einzelner Bauteile)
- `kalibrieren.py`, `drehzahl_test.py`, `bremsen_test.py` (Kalibrierung und Messung)
- `main.py` (Hinfahrt, sanftes Bremsen, Wand mit Stoßschalter berühren, Rückfahrt zur Startwand über die Encoder)
