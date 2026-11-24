# Abgabe Dokumentation / Projektbericht: Checkliste

| | |
| --- | --- |
| Projekt | ECHO, Mobiler Roboter für den Wall-Sprint (TechPioneers) |
| Dokument | `doku/abgabe_checkliste.md` |
| Stand | 24.11.2026, abends |

Abgabe über Moodle als **eine ZIP-Datei pro Gruppe**. Inhalt und Ordner der ZIP stehen in `doku/abgabe_readme.md` (in der ZIP als `README.pdf`). Text-Dokumente nur als PDF, CAD, Zeichnung, Code und Pläne im Format des jeweiligen Programms.

Status: ✅ fertig, 🟡 fertig bis auf Werte aus der Abnahme, ❌ fehlt noch

## Übersicht

| Nr. | Gefordert | Status | Wo |
| --- | --- | --- | --- |
| 1 | README: Beschreibung des ZIP-Inhalts | ✅ | `doku/abgabe_readme.md`, in der ZIP `README.pdf` |
| 2 | Projekttagebücher jeder Person (PDF) | ✅ | nur in der ZIP (`01_Projekttagebuecher/`), nicht im öffentlichen Repository |
| 3 | Benutzerdokumentation (PDF) | 🟡 | `doku/ECHO-Benutzerdokumentation.docx` / `.pdf` |
| 4 | Entwicklerdokumentation (PDF) mit CAD-Entwürfen, Programmcode, Schalt- und Verdrahtungsplan | ✅ | `doku/ECHO-Entwicklerdokumentation.docx` / `.pdf`, Abschnitte 2, 3 und 4 |
| 5 | Projektverlauf mit Phasen, Teilergebnissen, Herausforderungen, Fotos, wer hat was gemacht (PDF) | 🟡 | `doku/ECHO-Projektverlauf-Wochen.docx` / `.pdf`, Abschnitt 5 „Wer hat was gemacht“ |
| 6 | Vollständige CAD-Entwürfe in PTC Creo (Baugruppe Roboter) | ✅ | Creo-Originaldateien in `05_CAD_Creo/creo/` der ZIP (nicht im Repository), Baugruppenzeichnung als PDF; STEP und STL in `05_CAD_Creo/step_stl/` |
| 7 | Technische Zeichnung des Chassis (laser-schneidbar) | ✅ | `cad/zeichnung/2026-11-23_Grundplatte_V3_Zeichnung.pdf`, `cad/Grundplatte_V2_Laser.dxf` / `.svg` |
| 8 | Vollständiger Programmcode | ✅ | `code/main.py` (= `wallsprint_schnell.py`), frühere Stände, `code/tests/` |
| 9 | Vollständiger Schalt- oder Verdrahtungsplan | ✅ | `elektronik/schaltplan_v2.pdf` (gilt), `elektronik/steckbrett_v2.svg` / `.png` |
| 10 | Sonstige Dokumente | 🟡 | Präsentationen, Projektkarte, Protokoll, Messwerte, Testtabelle, Materialliste, Maßtabelle, Datenblätter, Fotos, Marketing |

## Noch zu tun

- [ ] **Nach der Abnahme am 25.11.:** seitliche Abweichung in die Zusammenfassung der Benutzerdokumentation, falls gemessen; Ablauf und Ergebnis der Abnahme in Woche 7 des Projektverlaufs; dann bei Benutzerdoku, Entwicklerdoku und Projektverlauf Version 1.0.0, Status „verabschiedet“
- [ ] **Präsentationen:** Folien vom 13.11. (KW 46), 20.11. (KW 47) und der Abschlusspräsentation am 27.11. als PDF nach `doku/praesentationen/` und in `09_Sonstiges/`
- [ ] **Beim Veranstalter klären:** Podest unter der Schale, Finnen der Haube über der Freiraumgrenze, Wippschalter als Startknopf. Antworten in Benutzer- und Entwicklerdoku eintragen
- [ ] **Tagebücher gegenlesen:** Felix seinen Eintrag 11. bis 13.11. (Podest) und 19.11. (Zeichnung zusammen mit Jaskaran), Kevin den Eintrag 12.11. (alle drei Echo-Halterungen)
- [ ] Zeichnung in Creo (optional): Ordinate x 236 ergänzen, Maß 5 an der Isometrie löschen, Podest-Loch auf x 56,26
- [ ] Einer aus dem Team lädt die ZIP hoch

## Erledigt am 24.11.

- Creo-Originaldateien (Stand 24.11., je Datei nur die neueste Version) in `05_CAD_Creo/creo/` der ZIP, Baugruppenzeichnung als PDF in `05_CAD_Creo/`, Zeichnung der Grundplatte mit Stand 24.11. (PDF und `grundplatte.drw`) in `06_Zeichnung_Chassis/`
- Messfahrt: 6,7 s für 200 cm hin und zurück, im Schnitt ca. 0,60 m/s. Eingetragen in Benutzerdoku, Entwicklerdoku, Projektverlauf, Messwerte und Testtabelle
- Comic-Cover mit Ø-Tempo 0,60 m/s, Comic-Strip mit Fahrzeit und Tempo, Bremspunkt im Comic auf 45 cm korrigiert

- Abgabestand des Codes als `code/main.py`, alte `main.py` als `main_2026-11-03.py`, Pinbelegung nach Schaltplan v2
- Schaltplan v2 mit Schriftfeld und Akku-Angabe
- Grundplatte: gelasert und verbaut ist die **V2** (47 Löcher), das bereinigte Modell mit 37 Löchern heißt **V3** (`cad/Grundplatte_V3.stp`, Zeichnung zeigt V3)
- Darstellung der Projektergebnisse aufgeteilt in Benutzer- und Entwicklerdokumentation; Entwicklerdoku mit Beschreibung aller CAD-Entwürfe, Bild der Baugruppe, Schaltplan, neuem Programmablaufplan und dem Programmcode Abschnitt für Abschnitt
- Projektverlauf: Abschnitt „Wer hat was gemacht“, Wochen 6 und 7 ergänzt, Platzhalter gefüllt
- Tagebücher formal korrigiert (Seitenzahlen, Status, Dateinamen) und die Zuordnung bei Zeichnung, Podest und Echo-Halterungen angeglichen
