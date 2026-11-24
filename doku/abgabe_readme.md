# ECHO, Mobiler Roboter für den Wall-Sprint: Inhalt der Abgabe

Gruppe TechPioneers (Team Batman): Felix Schurwanz, Jaskarnvir Singh, Kevin Rundt, Arda Dogan
Study Bootcamp Technik, FH Wedel, Wintersemester 2026/27, Prof. Dr. U. Hoffmann
Repository: github.com/trpbabos-jpg/Tech-pioneers-

ECHO fährt von der Startwand 200 cm geradeaus auf eine Zielwand zu, bremst davor sanft ab, berührt die Wand mit seinem Stoßschalter und fährt rückwärts zur Startwand zurück. Ein Tischtennisball in einer Schale auf dem Roboter darf dabei nicht herausfallen.

## Inhalt der ZIP

| Ordner bzw. Datei | Inhalt | Gefordert als |
| --- | --- | --- |
| `README.pdf` | diese Übersicht | Beschreibung des Inhalts |
| `01_Projekttagebuecher/` | Projekttagebücher von Jaskarnvir Singh, Kevin Rundt, Felix Schurwanz und Arda Dogan | Projekttagebücher jeder Person |
| `02_Benutzerdokumentation.pdf` | Überblick, Sicherheit, Inbetriebnahme und Eingangstest, Bedienung, Fehlerbehebung, Außerbetriebnahme | Benutzerdokumentation |
| `03_Entwicklerdokumentation.pdf` | Wartung und Einrichtung; Abschnitt 2 Beschreibung der CAD-Entwürfe; Abschnitt 3 Schalt- und Verdrahtungsplan; Abschnitt 4 Beschreibung des Programmcodes; bestehende Probleme; Weiterentwicklung | Entwicklerdokumentation |
| `04_Projektverlauf.pdf` | Projektphasen, jede Woche mit Ziel, Ergebnis und Reflexion, Teilergebnisse, Herausforderungen, Fotos und frühe Entwürfe; Abschnitt 5 „Wer hat was gemacht“ | Darstellung des Projektverlaufs |
| `05_CAD_Creo/creo/` | Creo-Originaldateien: Baugruppe `batmobile-v2.asm` mit allen Teilen (`.prt`), Unterbaugruppe `haube_v8.asm`, Zeichnungen `batmobile-v2.drw` und `grundplatte.drw` | CAD-Entwürfe in PTC Creo |
| `05_CAD_Creo/step_stl/` | ganzer Roboter als STEP, STL und GLB mit Ansichten; Haube V4 als STEP und STL; Echo-Halterungen als STL; Grundplatte V3 als STEP | CAD-Entwürfe (zum Ansehen ohne Creo) |
| `06_Zeichnung_Chassis/` | technische Zeichnung der Grundplatte V3 (BAT01.3.001.1, A3, 1:1) als PDF; Laserdatei der gelaserten Grundplatte V2 als DXF und SVG | technische Zeichnung des Chassis, laser-schneidbar |
| `07_Programmcode/` | `main.py` (Abgabestand, läuft auf dem ESP32), frühere Stände, `tests/` mit Testprogrammen, `einstellwerte.pdf` | vollständiger Programmcode |
| `08_Schaltplan/` | `schaltplan_v2.pdf` (gültiger Stand, Seite 2 mit Notizen), Steckplan `steckbrett_v2.svg` / `.png`, `pinbelegung.pdf` | Schalt- und Verdrahtungsplan |
| `09_Sonstiges/` | Präsentationen, Projektkarte, Projektprotokoll, Messwerte, Testtabelle, Materialliste, Maßtabelle (xlsx und PDF), Auszüge aus Datenblättern, Fotos, Mind Map, Marketing (Comic-Cover und Comic-Strip) | sonstige Dokumente |

## Programme zum Öffnen

- PDF: jeder PDF-Viewer
- Creo-Dateien: PTC Creo 13. Die Baugruppe `batmobile-v2.asm` aus dem Ordner `creo/` öffnen, dann findet sie alle Teile
- STEP und STL: jedes CAD-Programm, STL auch im Browser
- Programmcode: Thonny mit MicroPython für den ESP32. `main.py` wird unverändert auf den ESP32 kopiert (Entwicklerdokumentation, Abschnitt 1)
- DXF und SVG: Software des Lasercutters; SVG auch im Browser
- Maßtabelle: Excel oder LibreOffice Calc

## Hinweise

- Grundplatte: Gelasert und verbaut ist die Grundplatte **V2** mit 47 Löchern (Laserdatei). Das bereinigte Modell ohne die zehn nicht gebrauchten Löcher heißt **V3**; Creo-Modell und Zeichnung zeigen die V3.
- Schaltplan: Wo ältere Unterlagen (Steckplan, Protokoll, Tagebücher) andere Pins nennen, gilt der Schaltplan v2.
- Haube, Rohrblenden und das Modell des Wippschalters wurden mit KI erstellt; laut Prof. Hoffmann ist das erlaubt, wenn sie in Creo als Volumenkörper funktionieren.
