# Code

MicroPython für den ESP32. Nah an den Vorlesungsfolien (Kap. 4, 4a bis 4d).

- `main.py` ist das Fahrprogramm, das auf dem ESP32 läuft (Abgabestand 24.11.2026). Es ist dieselbe Datei wie `wallsprint_schnell.py`.
- Jeder funktionierende Zwischenstand bekommt eine eigene Datei. Ältere Stände: `fahren_v1_zustaende_hin_rueck.py`, `fahren_v2_vereinfacht.py`, `fahren_v3_vmax100.py` und `main_2026-11-03.py` (alte `main.py` mit Geradeausregelung über die Encoder, Pins vom 29.10.).
- Pins im Abgabestand nach `elektronik/schaltplan_v2.pdf`: Motor rechts 32 / 33 (M2A / M2B), Motor links 25 / 26 (M1A / M1B), Ultraschall vorne Trig 15 / Echo 39, Stoßschalter 27, Encoder links 13, rechts 14.
- Alle Einstellwerte mit Herkunft: `einstellwerte.md`.
