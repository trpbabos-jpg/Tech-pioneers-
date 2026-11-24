# Abgabe Dokumentation / Projektbericht: Checkliste

| | |
| --- | --- |
| Projekt | ECHO, Mobiler Roboter für den Wall-Sprint (TechPioneers) |
| Dokument | `doku/abgabe_checkliste.md` |
| Stand | 24.11.2026 |

Abgabe über Moodle als **eine ZIP-Datei pro Gruppe**. Wir müssen absprechen, wer hochlädt.

Regeln aus der Aufgabe:

- Alle Text-Dokumente **nur als PDF** (kein Word, OpenOffice, Pages). Also auch unsere `.md`-Dateien und `ECHO-Projektverlauf.docx` vor dem Packen als PDF exportieren.
- CAD-Entwürfe, technische Zeichnungen, Programmcode, Schalt- und Verdrahtungspläne im üblichen Format des Systems (Creo `.prt`/`.asm`/`.drw`, `.py`, `.svg` usw.).

Status: ✅ fertig, 🟡 da, aber noch nicht abgabefertig, ❌ fehlt noch

## Übersicht

| Nr. | Gefordert | Status | Was wir schon haben | Was noch fehlt |
| --- | --- | --- | --- | --- |
| 1 | README: Beschreibung des ZIP-Inhalts | ❌ | Repo-README und Ordner-READMEs als Vorlage | Eigene README für die ZIP schreiben, wenn die Struktur steht (Vorschlag unten) |
| 2 | Projekttagebücher jeder Person (PDF) | 🟡 | J führt sein Tagebuch, Datei wird am Projektende erstellt | Tagebücher von J, K, F und A als PDF einsammeln |
| 3 | Benutzerdokumentation (PDF) | 🟡 | `doku/ECHO-Projektkarte.pdf` (2 Seiten: Beschreibung, Inbetriebnahme, Erste Hilfe, Aufbau), Abschnitt „Code auf den ESP32 bringen“ im Repo-README | Eigene Benutzerdoku als PDF, siehe Punkt 3 unten |
| 4 | Entwicklerdokumentation (PDF) mit Mechanik, Programmierung, Elektronik | ❌ | Viel Material in Markdown verteilt im Repo | Ein zusammenhängendes PDF, siehe Punkt 4 unten |
| 5 | Projektverlauf mit Phasen, Teilergebnissen, Herausforderungen, Fotos, wer hat was gemacht (PDF) | 🟡 | `doku/ECHO-Projektverlauf.pdf`, Entwurf v0.2.0 vom 19.11., 6 Seiten mit Fotos und früher Formskizze | Stand ab 19.11., Tests, Abnahme, eigener Abschnitt „Wer hat was gemacht“, siehe Punkt 5 unten |
| 6 | Vollständige CAD-Entwürfe in PTC Creo (Baugruppe Roboter) | ❌ | Nur STEP-Exporte: `cad/Grundplatte_V2.stp`, `cad/haube_v4/Haube_V4.stp`, `cad/baugruppe/ECHO_Roboter_STEP.zip`, STL der Druckteile | Native Creo-Dateien und Baugruppe fertig machen, siehe Punkt 6 unten |
| 7 | Technische Zeichnung des Chassis (laser-schneidbar) | 🟡 | `cad/zeichnung/2026-11-23_Grundplatte_V2_Zeichnung_Entwurf.pdf`, `cad/Grundplatte_V2_Laser.dxf` | Zeichnung fertig, Lochzahl klären, Creo-`.drw` dazu, siehe Punkt 7 unten |
| 8 | Vollständiger Programmcode | 🟡 | `code/main.py`, Stände v1 bis v3, alle Testprogramme, `code/einstellwerte.md` | Finale `main.py` mit Pins nach Steckplan v2, getestet, siehe Punkt 8 unten |
| 9 | Vollständiger Schalt- oder Verdrahtungsplan | 🟡 | `elektronik/steckbrett_v2.svg` und `.png` (Stand 21.11.), `elektronik/pinbelegung.md`, Schaltplan im Miro-Board | Plan an den echten Aufbau anpassen und als Datei exportieren, siehe Punkt 9 unten |
| 10 | Sonstige wichtige Dokumente | 🟡 | Mind Map, Präsentationen bis 06.11., Messwerte, Testtabelle, Materialliste, Datenblätter, Fotos, Marketing | Fehlende Präsentationen und PDF-Exporte, siehe Punkt 10 unten |

## Was noch zu tun ist

### 1. README der ZIP

- Kurz das Projekt, das Team (Name und Kürzel) und welche Datei wo liegt
- Für jede geforderte Abgabe sagen, in welcher Datei sie steckt (Nr. 1 bis 10 oben)
- Welche Programme man zum Öffnen braucht (Creo, Thonny, PDF-Viewer)
- Link auf das GitHub-Repo
- Als `README.pdf` oder `README.txt`. Eine `.txt` ist kein Text-Dokument im Sinne von Word, im Zweifel beim Betreuer nachfragen

### 2. Projekttagebücher

- [ ] J: Tagebuch als PDF erstellen
- [ ] K: Tagebuch als PDF
- [ ] F: Tagebuch als PDF
- [ ] A: Tagebuch als PDF
- Dateinamen einheitlich, z. B. `Projekttagebuch_Singh.pdf`

### 3. Benutzerdokumentation

Die Projektkarte reicht wahrscheinlich nicht als Benutzerdoku, sie ist ein Steckbrief. Daraus ein eigenes PDF machen mit:

- [ ] Foto des fertigen Roboters
- [ ] Was ECHO kann (Hinfahrt, sanftes Bremsen, Antippen mit dem Stoßschalter, Rückfahrt)
- [ ] Lieferumfang und Bedienelemente (Wippschalter als Start, Stoßschalter, Akkufach)
- [ ] Akkus einsetzen und laden
- [ ] Aufstellen an der Startwand, Ball in die Schale, Start, 3 s Wartezeit
- [ ] Programm auf den ESP32 spielen (Thonny), Werte in `einstellwerte` ändern
- [ ] Haube und Schale ab- und aufbauen
- [ ] Fehlerbehebung (fährt schief, bremst zu spät, startet nicht, Stoßschalter löst beim Anfahren aus)
- [ ] Ablauf nach den letzten Tests prüfen

### 4. Entwicklerdokumentation

Aus dem vorhandenen Material ein PDF bauen. Gliederung nach der Aufgabe:

**Mechanik (CAD-Entwürfe)**
- [ ] Grundplatte v1 (Frankenstein-Modell) kurz, Grundplatte v2 ausführlich: Maße, Löcher, Koordinaten, Material und Laserwerte. Quelle: `cad/README.md`, `cad/grundplatte-v2-entscheidungen.md`
- [ ] Druckteile: Podest, Echo-Halterungen, Rohrblenden, Akku-Wanne, Steckbrett-Halter, Taster-Bügel, jeweils mit Zweck und Befestigung
- [ ] Haube V4: Teilung, Befestigung, Druckeinstellungen. Quelle: `cad/haube_v4/README.md`
- [ ] Baugruppe: Aufbau, Koordinatensystem, Masse und Schwerpunkt. Quelle: `cad/baugruppe/README.md`, `bom/Grundplatte_Masse_Gewicht_V2.xlsx`
- [ ] Bilder: Ansichten aus `cad/baugruppe/`, Zeichnung

**Programmierung**
- [ ] Programmablaufplan von `main.py` (fehlt noch ganz)
- [ ] Aufbau des Programms: Pins, Einstellwerte, Funktionen, die drei Schritte hinfahren, bremsen, zurückfahren
- [ ] Geradeausfahrt über die Encoder mit tempoabhängiger Korrektur, Bremsen über Ultraschall mit Median aus 3 Messungen, Stoßschalter, Rückfahrt über die Encoder
- [ ] Wie die Seitensensoren genutzt werden
- [ ] Testprogramme und wofür man sie braucht, Einstellwerte mit Herkunft. Quelle: `code/einstellwerte.md`, `code/tests/README.md`
- [ ] `code/README.md` ist bisher nur drei Zeilen lang, gleich mit ausbauen

**Elektronik (Schalt- und Verdrahtungsplan)**
- [ ] Bauteile mit Datenblattwerten. Quelle: `bom/materialliste.md`, `bom/datenblaetter/`
- [ ] Stromversorgung: Akku, Wippschalter, MDD3A, 5VO auf die rote Schiene, Grenze 200 mA
- [ ] Spannungsteiler für Echo (1 kΩ und 2,2 kΩ, ca. 3,4 V) mit Rechnung
- [ ] Pinwahl mit Begründung (Startpins frei, 34 bis 39 nur Eingang, interne Pull-ups). Quelle: `elektronik/pinbelegung.md`, Folien vom 23.10.
- [ ] Plan als Bild einfügen

### 5. Projektverlauf

`doku/ECHO-Projektverlauf.docx` weiterschreiben und am Ende als PDF exportieren (Version 1.0.0, Status verabschiedet).

- [ ] Stand nach dem 19.11. nachtragen: Haube anprobiert und geändert (20.11., 23.11.), Steckplan v2 (21.11.), technische Zeichnung (20. und 23.11.), Gesamtmodell (24.11.)
- [ ] Tests am Aufbau v2 mit Ergebnissen (Geradeausfahrt, Bremsen, Kipptest mit Ball, Geschwindigkeit auf 200 cm)
- [ ] Ergebnis der Abnahme (25.11.) und der Abschlusspräsentation (27.11.)
- [ ] **Eigener Abschnitt „Wer hat was gemacht“** mit allen vier Personen. Bisher steht das nur verteilt im Protokoll, und dort oft als „Team“
- [ ] Fehlende Zeiten und Kürzel im Protokoll (`doku/aenderungsverlauf.md`) nachtragen, jeder seine eigenen ab KW 45
- [ ] Fotos aus der Zeit nach dem 13.11. einfügen (Haube gedruckt, fertiger Roboter)
- [ ] Persönliches Fazit von jedem

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

### 9. Schalt- oder Verdrahtungsplan

- [ ] Prüfen, ob `steckbrett_v2` nach dem Umstecken genau dem echten Aufbau entspricht, sonst anpassen
- [ ] Plan für den ganzen Roboter, nicht nur das Steckbrett: Akku, Wippschalter, MDD3A, Motoren, Encoder, drei Sensoren, Stoßschalter
- [ ] Schaltplan aus dem Miro-Board auf den Stand v2 bringen und als PDF exportieren, oder einen Schaltplan in einem Elektronik-Programm (z. B. Fritzing) zeichnen und die Originaldatei mitgeben
- [ ] Pinbelegung: Tabelle „Stand 13.11.“ in `elektronik/pinbelegung.md` ausfüllen oder entfernen

### 10. Sonstige Dokumente

- [ ] Folien der Fortschrittspräsentationen vom 13.11. (KW 46) und 20.11. (KW 47) als PDF nach `doku/praesentationen/`
- [ ] Folien der Abschlusspräsentation (27.11.)
- [ ] Projektkarte fertig machen (Foto, Ablauf nach den Tests)
- [ ] Comic: Ø-Tempo auf dem Cover, Uhrzeit und Raum auf dem Strip
- [ ] Markdown-Dateien als PDF exportieren oder in die Entwicklerdoku übernehmen: Protokoll, Messwerte, Testtabelle, Materialliste, Einstellwerte, Entscheidungen Grundplatte
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
├── 02_Benutzerdokumentation.pdf
├── 03_Entwicklerdokumentation.pdf
├── 04_Projektverlauf.pdf
├── 05_CAD_Creo/            (alle .prt und die .asm, dazu STL der Druckteile)
├── 06_Zeichnung_Chassis/   (Zeichnung .pdf und .drw, Laserdatei .dxf)
├── 07_Programmcode/        (main.py, alle Stände, tests/)
├── 08_Schaltplan/          (Verdrahtungsplan .svg/.png, Schaltplan .pdf)
└── 09_Sonstiges/           (Präsentationen, Projektkarte, Protokoll, Messwerte,
                             Testtabelle, Materialliste, Datenblätter, Fotos, Marketing)
```

## Reihenfolge

1. Bis zur Abnahme am 25.11.: Code auf Steckplan v2 umstellen und testen (Punkt 8), damit die Demo läuft
2. Direkt danach: Ergebnisse in Projektverlauf und Benutzerdoku, Fotos vom fertigen Roboter
3. Creo-Baugruppe fertig machen und hochladen (Punkt 6), Zeichnung abschließen (Punkt 7)
4. Entwicklerdoku zusammenschreiben (Punkt 4), Schaltplan exportieren (Punkt 9)
5. Tagebücher einsammeln, README schreiben, alles als PDF exportieren, ZIP packen, einer lädt hoch
