# TechPioneers: Mobiler Roboter (Wall-Sprint)

Study Bootcamp Technik, FH Wedel, WS 2026/27

Ein kleiner, radgetriebener Roboter mit ESP32, der 200 cm geradeaus auf eine Wand zufährt und davor sanft abbremst. Bewertet werden die Basiseigenschaften **Geradeausfahrt** und **elegantes Abbremsen**, außerdem treten wir beim Wall-Sprint an.

## Team

| Kürzel | Name |
| --- | --- |
| J | |
| K | |
| F | |
| A | |

Planung (Kanban, Zeitplan, Regeln): Miro-Board unter der Mind Map
https://miro.com/app/board/uXjVEZ6PCT0=/

## Wo steht was

- Was wann passiert ist: `doku/aenderungsverlauf.md`
- Aktuelle Pinbelegung und frühere Stände: `elektronik/pinbelegung.md`
- Einstellwerte im Code: `code/einstellwerte.md`
- Messwerte: `doku/messwerte.md`
- Folien der Präsentationen: `doku/praesentationen/`
- Datenblätter der Bauteile: `bom/datenblaetter/`

## Termine

| Datum | Was |
| --- | --- |
| Fr 13.11.2026 | Fortschrittspräsentation |
| Fr 20.11.2026 | Fortschrittspräsentation |
| Mi 25.11.2026 | Abnahmegespräch mit Demo |
| Fr 27.11.2026 | Abschlusspräsentation |

## Ordner

| Ordner | Inhalt |
| --- | --- |
| `code/` | MicroPython-Programme für den ESP32, `main.py` ist das Fahrprogramm |
| `code/tests/` | Testprogramme für einzelne Bauteile (aufheben, werden wieder gebraucht) |
| `cad/` | Creo-Dateien (Teile und Baugruppe), technische Zeichnung als PDF, DXF für den Laser, Skizzen |
| `elektronik/` | Schaltplan und Pinbelegung |
| `bom/` | Materialliste, Auszüge aus den Datenblättern |
| `fotos/` | Fotos vom Aufbau und von Tests |
| `doku/` | Änderungsverlauf, Messwerte, Testtabelle, Mind Map, Präsentationen, später Projektkarte und Abschlussdoku |

## Code auf den ESP32 bringen

1. Thonny installieren (https://thonny.org) und den ESP32 per USB anschließen.
2. In Thonny unten rechts den Interpreter **MicroPython (ESP32)** und den richtigen Port wählen.
3. `code/main.py` öffnen und über *Datei > Speichern unter > MicroPython-Gerät* als `main.py` auf den ESP32 speichern.
4. ESP32 neu starten. Nach dem Einschalten wartet der Roboter 3 s und fährt dann los.

## Wie wir mit dem Repo arbeiten

- Nach jedem Schritt, der funktioniert und getestet ist, einen Commit machen.
- Commit-Nachricht kurz und klar, z. B. `v5 Geradeausfahrt kalibriert` oder `CAD Grundplatte v2 Löcher angepasst`.
- Programmstände eindeutig benennen, z. B. `fahren_v8_sanft_bremsen.py`. Alte Stände nicht löschen.
- Messwerte und Entscheidungen zusätzlich ins eigene Projekttagebuch.
- Am einfachsten mit GitHub Desktop (https://desktop.github.com), dann braucht man keine Kommandozeile.
