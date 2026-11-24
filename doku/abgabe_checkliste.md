# Abgabe Dokumentation / Projektbericht: Checkliste

| | |
| --- | --- |
| Projekt | ECHO, Mobiler Roboter für den Wall-Sprint (TechPioneers) |
| Dokument | `doku/abgabe_checkliste.md` |
| Stand | 24.11.2026, nachmittags (Projektverlauf v0.6.0 und Projektergebnisse v0.5.0 geprüft) |

Abgabe über Moodle als **eine ZIP-Datei pro Gruppe**. Wir müssen absprechen, wer hochlädt.

Regeln aus der Aufgabe:

- Alle Text-Dokumente **nur als PDF** (kein Word, OpenOffice, Pages). Also auch unsere `.md`-Dateien und die `.docx` vor dem Packen als PDF exportieren. Die PDFs im Repo sind mit LibreOffice erzeugt (andere Schrift), die endgültigen bitte aus Word exportieren.
- CAD-Entwürfe, technische Zeichnungen, Programmcode, Schalt- und Verdrahtungspläne im üblichen Format des Systems (Creo `.prt`/`.asm`/`.drw`, `.py`, `.svg` usw.).

Status: ✅ fertig, 🟡 da, aber noch nicht abgabefertig, ❌ fehlt noch

## Übersicht

| Nr. | Gefordert | Status | Was wir schon haben | Was noch fehlt |
| --- | --- | --- | --- | --- |
| 1 | README: Beschreibung des ZIP-Inhalts | ❌ | Repo-README und Ordner-READMEs als Vorlage | Eigene README für die ZIP schreiben, wenn die Struktur steht (Vorschlag unten) |
| 2 | Projekttagebücher jeder Person (PDF) | ❌ | J führt sein Tagebuch, Datei wird am Projektende erstellt | Tagebücher von J, K, F und A als PDF einsammeln |
| 3 | Benutzerdokumentation (PDF) | 🟡 | `doku/ECHO-Projektergebnisse.docx`, Zusammenfassung und Abschnitt 1: Geräteübersicht, technische Daten, Sicherheit, Inbetriebnahme, Eingangstest, Bedienung, Fehlerbehebung, Außerbetriebnahme. Dazu `doku/ECHO-Projektkarte.pdf` | Fotos vom echten Roboter, gemessene Werte, Platzhalter, siehe Punkt 3 |
| 4 | Entwicklerdokumentation (PDF) mit Mechanik, Programmierung, Elektronik | 🟡 | `doku/ECHO-Projektergebnisse.docx`, Abschnitte 2 bis 4: Wartung, Repository, Stückliste, Abhängigkeiten, Übertragen auf den ESP32, Entwicklertests, Architektur, Programmablaufplan, Code Abschnitt für Abschnitt, Elektronik, bestehende Probleme, Weiterentwicklung | Beschreibung der CAD-Entwürfe fehlt fast ganz, Code-Teil beschreibt noch die Pins vom 29.10., siehe Punkt 4 |
| 5 | Projektverlauf mit Phasen, Teilergebnissen, Herausforderungen, Fotos, wer hat was gemacht (PDF) | 🟡 | `doku/ECHO-Projektverlauf-Wochen.docx`, 23 Seiten: Termine, Phasen mit Zeitstrahl, jede Woche mit Ziel, Erkenntnis, gut und besser, Teilergebnisse, Abhängigkeiten, Herausforderungen, Fazit | **„Wer hat was gemacht“ fehlt ganz**, echte Fotos aus der Anfangszeit, Abnahme, siehe Punkt 5 |
| 6 | Vollständige CAD-Entwürfe in PTC Creo (Baugruppe Roboter) | ❌ | Nur STEP-Exporte: `cad/Grundplatte_V2.stp`, `cad/haube_v4/Haube_V4.stp`, `cad/baugruppe/ECHO_Roboter_STEP.zip`, STL der Druckteile | Native Creo-Dateien und Baugruppe fertig machen, siehe Punkt 6 |
| 7 | Technische Zeichnung des Chassis (laser-schneidbar) | 🟡 | `cad/zeichnung/2026-11-23_Grundplatte_V2_Zeichnung_Entwurf.pdf`, `cad/Grundplatte_V2_Laser.dxf` | Zeichnung fertig, Lochzahl klären, Creo-`.drw` dazu, siehe Punkt 7 |
| 8 | Vollständiger Programmcode | 🟡 | `code/main.py`, Stände v1 bis v3, alle Testprogramme, `code/einstellwerte.md` | Finale `main.py` mit Pins nach Steckplan v2, getestet, `taster_test.py`, siehe Punkt 8 |
| 9 | Vollständiger Schalt- oder Verdrahtungsplan | 🟡 | `elektronik/steckbrett_v2.svg` und `.png` (Stand 21.11.), `elektronik/pinbelegung.md`, Architekturbild in den Projektergebnissen, Schaltplan im Miro-Board | Plan an den echten Aufbau anpassen und den Schaltplan als Datei exportieren, siehe Punkt 9 |
| 10 | Sonstige wichtige Dokumente | 🟡 | Mind Map, Präsentationen bis 06.11., Projektkarte, Messwerte, Testtabelle, Materialliste, Datenblätter, Fotos, Marketing | Fehlende Präsentationen und PDF-Exporte, siehe Punkt 10 |

## Für beide Word-Dokumente

- [ ] Alle orangen Platzhalter in Klammern füllen (Projektverlauf 13, Projektergebnisse 16), dann Version 1.0.0, Status verabschiedet, Datum aktualisieren
- [ ] Den Kasten unter dem Dokumentkopf in eigenen Worten schreiben. Bisher steht dort wörtlich der Erklärtext der Vorlage. Bei den Projektergebnissen liest sich das komisch („welche Dinge dokumentiert werden sollten“)
- [ ] Commit 6b72283 am Ende durch den Commit des abgegebenen Stands ersetzen
- [ ] Am Ende aus Word als PDF exportieren und die PDFs im Repo ersetzen

## Was noch zu tun ist

### 1. README der ZIP

- Kurz das Projekt, das Team (Name und Kürzel) und welche Datei wo liegt
- Für jede geforderte Abgabe sagen, in welcher Datei und auf welchen Seiten sie steckt (Nr. 1 bis 10 oben)
- Welche Programme man zum Öffnen braucht (Creo, Thonny, PDF-Viewer)
- Link auf das GitHub-Repo und den abgegebenen Commit
- Als `README.pdf` (Text-Dokumente nur als PDF)

### 2. Projekttagebücher

- [ ] J: Tagebuch als PDF erstellen
- [ ] K: Tagebuch als PDF
- [ ] F: Tagebuch als PDF
- [ ] A: Tagebuch als PDF
- Dateinamen einheitlich, z. B. `Projekttagebuch_Singh.pdf`

### 3. Benutzerdokumentation

Inhaltlich deckt Abschnitt 1 der Projektergebnisse alle Fragen aus Kap. 7 ab. Es fehlen nur Werte und Bilder vom fertigen Roboter.

- [ ] Fotos vom echten Roboter mit Haube: Gesamtansicht, Wippschalter, Akkufach. Bisher sind es nur CAD-Bilder und der Comic
- [ ] Am fertigen Roboter messen und wiegen: Abmessungen mit Haube, Masse, Schalenrand über Boden
- [ ] Durchschnittsgeschwindigkeit auf 200 cm (3 Messungen)
- [ ] Wettbewerbsregeln eintragen, sobald geklärt (Podest, Haube und Freiraum, Wippschalter als Start)
- [ ] Ablauf und Eingangstest nach dem Umstecken auf Steckplan v2 noch einmal prüfen
- [ ] Optional: Link zum Video der Demo

### 4. Entwicklerdokumentation

**Mechanik (CAD-Entwürfe): die größte Lücke.** Die Abgabe verlangt eine Beschreibung der CAD-Entwürfe. Bisher gibt es dazu nur den Absatz „Mechanischer Aufbau“, die Zeichnung und die Fertigungsschritte. Ein eigener Unterabschnitt sollte enthalten:

- [ ] Aufbau der Creo-Baugruppe: welche Teile und Unterbaugruppen, Dateinamen, Koordinatensystem (Ursprung Mitte Radachse auf der Plattenoberseite), wie die Teile platziert sind
- [ ] Grundplatte v2: Maße, Lochbild mit Zweck der Löcher, warum 47 bzw. 37 Löcher. Quelle: `cad/grundplatte-v2-entscheidungen.md`
- [ ] Druckteile je mit Zweck, Hauptmaßen und Befestigung: Podest, Echo-Halterungen, Rohrblenden, Akku-Wanne, Steckbrett-Halter, Bedienpult, Taster-Bügel
- [ ] Haube V4: Teilung bei x 58, Befestigung H1 bis H7, Einschnitte für die Sensoren, Freiraum. Quelle: `cad/haube_v4/README.md`
- [ ] Wie man ein Teil ändert und neu exportiert (STEP, STL, DXF für den Laser)
- [ ] Bilder aus `cad/baugruppe/` (z. B. ohne Haube und mit Haube)

**Programmierung**
- [ ] Nach dem Umstecken den ganzen Code-Teil auf die neue `main.py` bringen: Pin-Tabelle, Ausschnitte (Abbildungen 10 bis 14), Einstellwerte
- [ ] Seitliche Sensoren: im Programm nutzen oder begründen, warum nicht. Sie sind verbaut, das wird bei der Abnahme bestimmt gefragt
- [ ] Ergebnisse der Entwicklertests am fertigen Roboter eintragen

**Elektronik**
- [ ] Pin-Tabelle vom 29.10. durch Steckplan v2 ersetzen
- [ ] Schaltplan als Bild einfügen, nicht nur auf das Miro-Board verweisen

**Abhängigkeiten**
- [ ] Versionen eintragen: MicroPython (`import os; os.uname()`), Thonny, Creo

**Getrennt abgeben:** Die Abgabe nennt Benutzerdoku und Entwicklerdoku als zwei PDFs. Am sichersten die Projektergebnisse komplett abgeben und zusätzlich als zwei Teile exportieren: Zusammenfassung mit Abschnitt 1 als Benutzerdokumentation, Abschnitte 2 bis 4 als Entwicklerdokumentation. Oder beim Betreuer fragen, ob ein Dokument mit Verweis in der README reicht.

### 5. Projektverlauf

- [ ] **Eigener Abschnitt „Wer hat was gemacht“** mit allen vier Personen. Die Abgabe verlangt das ausdrücklich, im Dokument steht bisher überall nur „wir“. Vorschlag: eine Tabelle Arbeitspaket gegen Person (Elektronik, Programm, Grundplatte v1 und v2, Podest, Halterungen, Haube, Zeichnung, Baugruppe, Doku, Präsentationen, Marketing) und bei jeder Woche eine Zeile „Wer“
- [ ] Wochen 1 bis 4 ehrlich darstellen: Bis zum 06.11. hat J allein gearbeitet (steht so im Protokoll), im Text steht aber „wir“
- [ ] Echte Fotos aus der Anfangszeit, falls vorhanden: Steckbrett (20.10.), Frankenstein-Modell (26. bis 29.10.), gedruckte Haube am Roboter (20.11. und 23.11.). Bisher zeigen die frühen Wochen nur Folien, Code und Skizzen, und die Haube nur als CAD-Bild
- [ ] Fortschrittspräsentation KW 47 am 20.11.: klären, ob sie stattgefunden hat, und den Platzhalter in der Terminübersicht ersetzen
- [ ] Woche 7 mit Abnahme (25.11.) und Abschlusspräsentation (27.11.) fertig schreiben
- [ ] Offene Lösungen eintragen: Steckhülsen am Stoßschalter, 47 oder 37 Löcher, Masse der Baugruppe, Räder in der Baugruppe
- [ ] Fehlende Zeiten und Kürzel im Protokoll (`doku/aenderungsverlauf.md`) nachtragen, jeder seine eigenen ab KW 45

### 6. CAD in PTC Creo

Im Repo liegen bisher nur STEP-Exporte. Gefordert ist die Baugruppe als Creo-Datei.

- [ ] Native Creo-Dateien aller Teile (`.prt`) und der Baugruppe `batmobile-v2` (`.asm`) hochladen. Vorher alte Versionen löschen (Datei > Verwalten > Alte Versionen löschen), damit keine `.prt.1`, `.prt.2` dabei sind
- [ ] Räder in der Baugruppe auf die Messung setzen (Reifen innen ±89,7 mm)
- [ ] Front der Haube gegen den Stand vom 23.11. tauschen
- [ ] Eins der zwei Motormodelle entfernen (`JGA25-370` oder `POLOLU-25D...`)
- [ ] Fehlende Teile ergänzen: Steckbrett mit ESP32, Bedienpult mit Wippschalter, Schale, Akku mit Wanne, Schrauben `SCHRAUBE_DIN_7991`
- [ ] Masse der Baugruppe korrigieren (zeigt 10,823 kg statt ca. 1,1 kg), Material PLA bzw. Sperrholz zuweisen
- [ ] Podest-Loch von x 56,0 auf 56,26 korrigieren
- [ ] STL des Podests hochladen
- [ ] Grundplatte v1: Creo-Dateien und Laserdatei hochladen (als früher Entwurf)
- [ ] Baugruppe einmal komplett in Creo öffnen und prüfen, dass nichts rot ist (fehlende Referenzen)
- Bei der Abgabe den Ordner mit allen Creo-Dateien so packen, dass die Baugruppe ihre Teile findet

### 7. Technische Zeichnung Chassis

- [ ] Offene Kleinigkeiten: Ordinate x 236 ergänzen, Maß 5 an der Isometrie löschen, „-0.5“ als „-0,5“, optional 8 durch Ordinate 248 ersetzen
- [ ] Koordinatentabelle mit x und y zusätzlich (Wunsch des Betreuers)
- [ ] Klären: gelaserte Platte und DXF haben 47 Löcher, Modell und Zeichnung 37. Zeichnung und Laserdatei müssen in der Abgabe zusammenpassen. Entweder DXF aus dem aktuellen Modell neu erzeugen oder die Zeichnung auf die gelaserte Platte bringen
- [ ] Zeichnung freigeben (Entwurf aus dem Dateinamen nehmen) und als PDF und Creo-`.drw` abgeben
- [ ] Laserdatei (`.dxf`) aus genau diesem Stand

### 8. Programmcode

`main.py` hat noch die Pins vom 29.10. und nur einen Ultraschallsensor.

- [ ] Nach Steckplan v2 umstecken und `main.py` anpassen (Motor rechts 32/33, links 25/26, Encoder 14 und 13, Echo 39, 36 und 4, Trig 15, 21 und 2, Taster 27)
- [ ] Drehrichtung, jeden Sensor und jeden Encoder einzeln testen
- [ ] Faktor für die Geradeausfahrt auf dem neuen Aufbau neu bestimmen
- [ ] Bremsen und Kipptest mit Ball
- [ ] Finalen Stand als eigene Datei sichern (z. B. `fahren_v4_drei_sensoren.py`) und als `main.py`
- [ ] `code/einstellwerte.md` mit den neuen Werten ergänzen
- [ ] Testprogramme an die neuen Pins anpassen oder vermerken, dass sie zum Stand 29.10. gehören
- [ ] `taster_test.py` ins Repo (beide Word-Dokumente sagen, dass es fehlt)

### 9. Schalt- oder Verdrahtungsplan

- [ ] Prüfen, ob `steckbrett_v2` nach dem Umstecken genau dem echten Aufbau entspricht, sonst anpassen
- [ ] Plan für den ganzen Roboter, nicht nur das Steckbrett: Akku, Wippschalter, MDD3A, Motoren, Encoder, drei Sensoren, Stoßschalter
- [ ] Schaltplan aus dem Miro-Board auf den Stand v2 bringen und als PDF exportieren, oder einen Schaltplan in einem Elektronik-Programm (z. B. Fritzing) zeichnen und die Originaldatei mitgeben
- [ ] Pinbelegung: Tabelle „Stand 13.11.“ in `elektronik/pinbelegung.md` ausfüllen oder entfernen

### 10. Sonstige Dokumente

- [ ] Folien der Fortschrittspräsentationen vom 13.11. (KW 46) und 20.11. (KW 47) als PDF nach `doku/praesentationen/`
- [ ] Folien der Abschlusspräsentation (27.11.)
- [ ] Projektkarte: Foto vom echten Roboter statt CAD-Bild
- [ ] Comic: Ø-Tempo auf dem Cover, Uhrzeit und Raum auf dem Strip
- [ ] Markdown-Dateien als PDF exportieren: Protokoll, Messwerte, Testtabelle, Materialliste, Einstellwerte, Entscheidungen Grundplatte
- [ ] `bom/Grundplatte_Masse_Gewicht_V2.xlsx` zusätzlich als PDF
- [ ] `elektronik/steckplan.html` ist ein alter Stand, als PNG reicht

## Vorschlag für die ZIP-Struktur

```
TechPioneers_ECHO_Abgabe.zip
├── README.pdf
├── 01_Projekttagebuecher/
│   ├── Projekttagebuch_Singh.pdf
│   ├── Projekttagebuch_Rundt.pdf
│   ├── Projekttagebuch_Schurwanz.pdf
│   └── Projekttagebuch_Dogan.pdf
├── 02_Benutzerdokumentation.pdf      (Projektergebnisse: Zusammenfassung und Abschnitt 1)
├── 03_Entwicklerdokumentation.pdf    (Projektergebnisse: Abschnitte 2 bis 4)
├── 04_Projektverlauf.pdf             (ECHO-Projektverlauf-Wochen)
├── 05_Projektergebnisse_komplett.pdf
├── 06_CAD_Creo/            (alle .prt und die .asm, dazu STL der Druckteile)
├── 07_Zeichnung_Chassis/   (Zeichnung .pdf und .drw, Laserdatei .dxf)
├── 08_Programmcode/        (main.py, alle Stände, tests/)
├── 09_Schaltplan/          (Verdrahtungsplan .svg/.png, Schaltplan .pdf)
└── 10_Sonstiges/           (Präsentationen, Projektkarte, Protokoll, Messwerte,
                             Testtabelle, Materialliste, Datenblätter, Fotos, Marketing)
```

## Reihenfolge

1. Bis zur Abnahme am 25.11.: Code auf Steckplan v2 umstellen und testen (Punkt 8), damit die Demo läuft. Fotos vom fertigen Roboter machen, auch von Haube, Schalter und Akkufach
2. Gleich danach: Aufgabenverteilung mit allen vier klären und „Wer hat was gemacht“ schreiben (Punkt 5), solange alle es noch wissen
3. Creo-Baugruppe fertig machen und hochladen (Punkt 6), Zeichnung abschließen (Punkt 7), daraus den CAD-Abschnitt der Entwicklerdoku schreiben (Punkt 4)
4. Ergebnisse von Abnahme und Tests in beide Word-Dokumente, Platzhalter füllen, Schaltplan exportieren (Punkt 9)
5. Tagebücher einsammeln, README schreiben, alles als PDF exportieren, ZIP packen, einer lädt hoch
