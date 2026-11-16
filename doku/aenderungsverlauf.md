# Projektprotokoll

| | |
| --- | --- |
| Projekt | ECHO, Mobiler Roboter für den Wall-Sprint (TechPioneers) |
| Dokument | `doku/aenderungsverlauf.md` |
| Version | 0.3.0 |
| Datum | 16.11.2026 |
| Status | Entwurf |

Gemeinsames Protokoll der Gruppe: was wann passiert ist, wer dran war, wie lange es gedauert hat, welche Entscheidungen wir getroffen haben und was noch offen ist. Es ist die Grundlage für die Dokumentation des Projektverlaufs (Vorlage Kap. 7). Das persönliche Projekttagebuch führt jeder zusätzlich selbst und gibt es über Moodle ab.

**Neue Einträge:** eine Zeile in der Übersicht und darunter ein Eintrag mit Details. Wer: J, K, F, A oder mehrere (z. B. J, K). Zeit: tatsächliche Arbeitszeit, bei mehreren Leuten pro Person. Bis zum 06.11. war J allein am Projekt.

## Übersicht

| Datum | Wer | Zeit | Was | Art | Verweis |
| --- | --- | --- | --- | --- | --- |
| 15.10. | J | 2 h | Mind Map zum Roboter | Kreativtechnik | `doku/mindmap_v1.pdf` |
| 16.10. | J | nicht erfasst | Ideen-Pitch im Plenum | Präsentation | `doku/praesentationen/2026-10-16_pitch.pdf` |
| 19.10. | J | 1 h | Testprogramme für Ultraschall und Motor | Programmierung | `code/tests/` |
| 20.10. | J | 5 h | Steckbrett verkabelt, Ultraschall getestet, MDD3A und Motoren angeschlossen, Stopp bei 30 cm, Schaltplan im Miro | Hardware / Test / Doku | `elektronik/pinbelegung.md` |
| 22.10. | J | 1 h 20 min | Taster gelernt, Lab-Aufgaben, Taster verkabelt | Lernen / Programmierung | Kap. 4c |
| 23.10. | J | ca. 2 h | Encoder angeschlossen, Drehzahl gemessen, Pinwahl belegt, Folien | Hardware / Programmierung / Recherche | `doku/praesentationen/2026-10-23_encoder-pins.pdf` |
| 26.10. | J | 1 h 30 min | Grundplatte v1 in Creo konstruiert und gelasert | Konstruktion / Fertigung | `cad/README.md` |
| 27.10. | J | ca. 1 h | Löcher für die Stützkugel, Räder montiert | Konstruktion / Montage | |
| 27. bis 28.10. | J | ca. 3 h | Neu verkabelt ohne Kabelkreuzungen | Hardware / Entscheidung | `elektronik/pinbelegung.md` |
| 29.10. | J | ca. 1 h 40 min, Vormittag offen | Drehrichtung korrigiert, neu kalibriert, Vmax und Bremsen gemessen, erste Fahrt mit main.py | Kalibrierung / Test | `code/einstellwerte.md`, `doku/messwerte.md` |
| 30.10. | J | nicht erfasst | main.py vereinfacht, Präsentation Frankenstein-Modell | Programmierung / Präsentation | `code/fahren_v2_vereinfacht.py` |
| 03.11. | J | nicht erfasst | Schneller fahren, Korrektur abhängig vom Tempo | Programmierung / Test | `code/main.py` |
| 05.11. | J | 45 min abends, Rest offen | Maßtabelle, Konzept Grundplatte v2 | Konstruktion / Entscheidung | `bom/Grundplatte_Masse_Gewicht_V2.xlsx` |
| 06.11. | J | 1 h 25 min Präsentation, Rest offen | Grundplatte v2 fertig zum Lasern, Weekly Closing KW 45, Gruppe zu viert, Kanban, Zeitplan, Repository | Konstruktion / Präsentation / Organisation | `cad/grundplatte-v2-entscheidungen.md` |
| 09.11. | Team | offen | Grundplatte v2 gelasert, erster Aufbau | Fertigung / Montage | `fotos/2026-11-09_*` |
| 10.11. | Team | offen | 13 Aufgaben als Issues, Kanban und Zeitplan ergänzt | Organisation | GitHub-Issues, Miro-Board |
| 11. bis 13.11. | Team | offen | Schalen-Podest in Creo | Konstruktion / Messung | `cad/skizzen/2026-11-11_podest_schnitt.png` |
| 13.11. | Team | offen | Echo-Halterung, Elektronik verkabelt, CAD-Baugruppe teilweise, Fortschrittspräsentation KW 46 | Montage / Konstruktion / Präsentation | `fotos/2026-11-13_*` |

## Einträge

### KW 42

**15.10.2026: Mind Map**
- Ideen zum Roboter in einer Mind Map gesammelt (Miro-Board „Roboter Mind Map“)

**16.10.2026: Pitch**
- Idee, Bauteilrecherche und Mind Map (`doku/mindmap_v1.pdf`, Miro-Board) vorgestellt
- Thema Batman: Ultraschall wie die Echoortung einer Fledermaus
- Folien: `doku/praesentationen/2026-10-16_pitch.pdf`, Datenblatt-Auszüge: `bom/datenblaetter/`
- Erste Formskizze ECHO: Differentialantrieb mit je einem Rad links und rechts, Stützkugel vorne (`cad/skizzen/2026-10-16_echo_form_draufsicht.png`)

### KW 43

**19.10.2026: erster Code**
- Testprogramme für Ultraschallsensor und Motor geschrieben
- Entscheidung: Motor und Ultraschall erst in getrennten Programmen testen, damit sich Fehler einem Bauteil zuordnen lassen

**20.10.2026: Steckbrett aufgebaut**
- ESP32, HC-SR04 mit Spannungsteiler und LED verkabelt, `ultraschall_test.py` läuft
- Problem: GPIO2 war nicht mit der LED verbunden, und der 1-kΩ-Widerstand steckte eine Spalte zu weit. Beides behoben
- Motortreiber MDD3A und beide Motoren angeschlossen, Akku über Schalter
- Beide Motoren getestet, kombinierter Code stoppt bei 30 cm Abstand
- Schaltplan und Kabelübersicht im Miro-Board angelegt
- Entscheidung: Sensor bekommt Strom über die Schienen, damit später mehr Sensoren dazukommen können
- Entscheidung: Akku nur an VB+ und VB−, 5VO am MDD3A bleibt frei, vor dem Umstecken Schalter aus und USB ab
- Pinbelegung: `elektronik/pinbelegung.md`

**22.10.2026: Taster**
- Taster-Code gelernt und die Lab-Aufgaben aus Kap. 4c gelöst
- Taster an GPIO27 und GND, im Code mit internem Pull-up. Der Taster ist ein Öffner: gedrückt ergibt 1

**23.10.2026: Encoder und Pinwahl**
- Encoder beider Motoren an 13, 14, 19 und 4, Versorgung mit 3,3 V statt 5 V, damit keine 5-V-Signale am ESP32 ankommen
- GPIO18 verworfen, weil es ihn auf dem ESP32-PICO-V3 nicht gibt
- Entscheidung: GPIO12 und die anderen Startpins bleiben frei
- Pinwahl mit Herstellerunterlagen begründet (Folien: `doku/praesentationen/2026-10-23_encoder-pins.pdf`)
- Drehzahlmessung über die Encoder: 244 und 247 U/min (`doku/messwerte.md`)

### KW 44

**26.10.2026: Frankenstein-Modell**
- Grundplatte v1 in Creo konstruiert und aus 5 mm Sperrholz gelasert, Motoren oben auf der Platte, Stützrad vorne
- Entscheidung: Aufbau bleibt abbaubar, die Verkabelung bleibt auf dem Steckbrett mit dem ESP32
- Entscheidung: Motorwinkel an den Randkerben über Kreuz verschraubt, weil in der Mitte keine Mutter passt
- Dient als fahrtüchtiger Prototyp für Encoder-Tests und Kalibrierung

**27. bis 28.10.2026: Räder und neue Verkabelung**
- Löcher für die Stützkugel ergänzt, Räder montiert
- Steckbrett komplett neu belegt, damit sich keine Kabel kreuzen (`elektronik/pinbelegung.md`)
- Entscheidung: Die rote Schiene bleibt 5 V, damit später mehrere Ultraschallsensoren dazukommen können

**29.10.2026: kalibriert und erste Fahrt**
- Fehler gefunden: Räder drehten gegeneinander, Ursache war die Verkabelung, behoben über `RICHTUNG_RECHTS`
- Kalibrierung: Anlauf 20 %, Faktor links 0,94 (`code/einstellwerte.md`)
- Erste Fahrt auf dem Boden mit sanftem Bremsen, Stopp bei 13,1 cm
- Problem: Der Stoßschalter löste beim Anfahren aus. Lösung: Taster pro Takt mehrfach lesen
- Rückfahrt eingebaut: rückwärts über die Encoder zur Startwand, ohne Wenden

**30.10.2026: main.py vereinfacht**
- Statt der Zustände nur noch drei Schritte: hinfahren, sanft bremsen bis der Stoßschalter auslöst, rückwärts dieselbe Strecke zurück
- Ultraschall über den Median der letzten 3 Messungen
- Erkenntnis: Der Ultraschall sitzt ca. 10 cm hinter dem Stoßschalter, deshalb Bremsbeginn später auf 45 bis 50 cm
- Code: `code/fahren_v2_vereinfacht.py`
- Folien: `doku/praesentationen/2026-10-30_frankenstein-modell-und-encoder.pdf`

### KW 45

**03.11.2026: schneller fahren, Korrektur abhängig vom Tempo**
- Erst VMAX 100 ausprobiert (`code/fahren_v3_vmax100.py`), dann VMAX 80 und Kriechen 20 %
- Beim Kriechen an der Wand fuhr er schief, weil die Korrektur von ±8 % bei 20 % zu stark war. Jetzt wird die Grenze mit dem Tempo kleiner
- Eigener Faktor links für die Rückfahrt (`FAKTOR_LINKS_ZURUECK`)
- Faktor links auf 0,7 gesetzt, gleicht die Mechanik aus, wird mit der Grundplatte v2 neu bestimmt
- Test mit gestapelten Stühlen als Wand: Ultraschall misst unruhig, weil die Wand uneben ist, nicht wegen des Codes
- Aktueller Stand: `code/main.py`, Werte in `code/einstellwerte.md`

**05.11.2026: Grundplatte v2 geplant**
- Maßtabelle mit allen Bauteilen, Gewichten und offenen Maßen angelegt (`bom/Grundplatte_Masse_Gewicht_V2.xlsx`)
- Freiraumregel ausgewertet: Schalenrand 105 mm über Boden, alles andere bleibt unter 85 mm
- Entscheidung: Variante „Turm“, die Schale sitzt auf einem gedruckten Podest über dem Schwerpunkt. Die Variante mit tiefer Schale ganz vorne wurde verworfen

**06.11.2026: Grundplatte v2 fertig zum Lasern**
- Kein Klett mehr, alle Halterungen 3D-gedruckt und mit M3 verschraubt
- Drei Ultraschallsensoren statt einem, weil die Seitenwände nicht gerade sind
- Wippschalter wird Hauptschalter und Startknopf, der Code wartet nach dem Booten 3 s
- Rückwand gestrichen, das Heck der Batmobil-Haube wird die Anlagefläche an der Startwand
- 7 Löcher für die Haube, MDD3A direkt mit 4 × M3 auf Abstandshülsen, keine Langlöcher mehr
- Laserdatei und Maßtabelle hochgeladen (`cad/`, `bom/`), Entscheidungen in `cad/grundplatte-v2-entscheidungen.md`
- Weekly Closing KW 45: `doku/praesentationen/2026-11-06_weekly-closing-kw45.pdf` (die drei Testvideos sind im PDF nur als Standbild)
- Gruppe ist jetzt zu viert. Planung mit Kanban und Zeitplan im Miro-Board, dieses Repository angelegt

### KW 46

**09.11.2026: Grundplatte v2 gelasert und erster Aufbau**
- Platte aus 5 mm Sperrholz gelasert, alle Löcher passen
- Motoren, Kugelrolle, MDD3A, Stoßschalter und Akku probeweise aufgebaut (Fotos in `fotos/`, 09.11.)
- Problem: Die M2-Schrauben der Kugelrolle stehen oben über, der Stoßschalter lag darauf und kippte nach vorne. Umdrehen ging nicht, weil die Schrauben dann die Kugel berühren
- Lösung: unter beide Schrauben des Stoßschalters je zwei M3-Muttern gestapelt, er steht jetzt gerade ca. 5 mm höher
- Problem: Der Stoßschalter ist mit Flachsteckhülsen 50 bis 55 mm lang und kommt der Akku-Wanne in die Quere. Lösung offen: gewinkelte Steckhülsen oder Akku-Wanne bis 8 mm nach hinten
- Entscheidung: Die zwei langen M3-Schrauben des Stoßschalters tragen gleich den Halter für den vorderen Ultraschallsensor

**10.11.2026: Aufgaben bis zur Abnahme**
- 13 Aufgaben als Issues angelegt, mit Meilenstein „Abnahme 25.11.2026“, und im Miro-Kanban und Zeitplan ergänzt
- Steckbrett als STEP-Modell für Creo besorgt

**11. bis 13.11.2026: Schalen-Podest in Creo**
- Drehteil: Fuß Ø58 × 4, Rohr Ø36 (innen Ø30), Kopf Ø62 × 4, Kopf-Oberkante 69,2 mm über der Platte, 45°-Fase unter dem Kopf, damit es ohne Stützmaterial druckt
- 4 Rippen zwischen Rohr und Fuß, 4 Durchgangslöcher Ø3,4 im Fuß, 6 Kernlöcher Ø2,7 im Kopf für die Laschen der Schale
- Gemessen: Schale am Rand ca. Ø101, Lochkreis der Laschen ca. Ø49, Akkupack 17,5 mm hoch
- Problem: Das Rohr war in Creo zuerst nur halb so breit, weil ein Maß als Durchmesser statt als Radius eingetragen war. Behoben
- Skizze: `cad/skizzen/2026-11-11_podest_schnitt.png`

**13.11.2026: Echo-Halterung, Verkabelung, CAD-Baugruppe**
- Echo-Halterung für den vorderen Ultraschallsensor gedruckt und montiert, sie sitzt auf den Schrauben des Stoßschalters
- Räder montiert und Elektronik auf der Grundplatte v2 komplett angeschlossen (Foto: `fotos/2026-11-13_elektronik_verkabelt.jpg`)
- CAD-Baugruppe des Roboters in Creo teilweise fertig: Grundplatte v2, Motoren mit Winkeln, Räder, Kugelrolle, MDD3A, Steckbrett mit ESP32, Podest für die Schale, drei Ultraschallsensoren mit Haltern. Screenshots in `fotos/2026-11-13_cad_baugruppe/`
- Noch nicht in der Baugruppe: Haube, Akku mit Wanne, Bedienpult mit Wippschalter, Stoßfänger
- Fortschrittspräsentation KW 46: Umbau, Kanban, GitHub, Echo-Halterung und Podest

## Offene Punkte

- Code am neuen Roboter testen, Faktor für die Geradeausfahrt neu bestimmen (Gewicht und Aufbau haben sich geändert)
- Ultraschall und Bremsen auf dem neuen Aufbau nachtesten, Kipptest mit Ball
- Neue Pinbelegung mit drei Ultraschallsensoren in `elektronik/pinbelegung.md` eintragen
- Probedruck für die M3-Löcher, danach Halter drucken
- Akku-Wanne, Steckbrett-Halter und Taster mit größerem Kontaktpunkt modellieren
- Schaltplan, Programmablaufplan und Creo-Baugruppe fertig machen
- Messen: Stößelspitze bis Plattenvorderkante, Spurweite, Motorlänge mit Encoder
- Taster-Kabel: gewinkelte Steckhülsen oder Akku-Wanne verschieben
- Geschwindigkeit auf 200 cm messen (3 Mal)
- Beim Veranstalter klären: Podest unter der Schale, Wippschalter als Start, Sensoren an Start- und Endwand
- Fehlende Zeiten und Kürzel in der Übersicht nachtragen

## Wiedervorlagen

| Datum | Was |
| --- | --- |
| Fr 20.11.2026 | Fortschrittspräsentation KW 47 |
| Mi 25.11.2026 | Abnahmegespräch mit Demo |
| Fr 27.11.2026 | Abschlusspräsentation |
| bis Projektende | Projekttagebuch und Projektbericht über Moodle |

## Zeitaufwand

Bisher nur aus dem Tagebuch von J übernommen. Bitte jeder seine Zeiten ab KW 45 ergänzen.

| Woche | Zeitraum | Zeit |
| --- | --- | --- |
| KW 42 | bis 16.10. | 2 h |
| KW 43 | 19. bis 23.10. | ca. 9 h 20 min |
| KW 44 | 26. bis 30.10. | ca. 7 h 10 min, ohne 29.10. vormittags und 30.10. |
| KW 45 | 02. bis 06.11. | ca. 2 h 10 min erfasst, Rest offen |
| KW 46 | 09. bis 13.11. | noch nicht erfasst |
| Summe | | ca. 20 h 40 min erfasst |
