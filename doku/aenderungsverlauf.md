# Projektprotokoll

| | |
| --- | --- |
| Projekt | ECHO, Mobiler Roboter für den Wall-Sprint (TechPioneers) |
| Dokument | `doku/aenderungsverlauf.md` |
| Version | 0.6.5 |
| Datum | 24.11.2026 |
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
| 17. bis 18.11. | J | offen | Haube V4: Entwurf, Befestigung, Anpassung an Quarz und echte Halterungen, fertige STEP für Creo, Druck vorbereitet | Konstruktion / Entscheidung / Fertigung | `cad/haube_v4/` |
| KW 47, bis 20.11. | Team | offen | Projektkarte, Dokumentation des Projektverlaufs (Entwurf), Marketing: Comic-Cover und Comic-Strip | Dokumentation / Marketing | `doku/ECHO-Projektkarte.pdf`, `doku/ECHO-Projektverlauf-Wochen.pdf`, `doku/marketing/` |
| 20.11. | J | offen | Haube gedruckt und anprobiert, Räder gemessen, Haube geändert: Radkasten offen, Teilung bei x 58 | Fertigung / Messung / Konstruktion | `cad/haube_v4/` |
| 20.11. | J | offen | Technische Zeichnung Grundplatte begonnen, Rückmeldung Betreuer, Bohrungen im Modell vereinheitlicht und 10 gelöscht | Konstruktion / Dokumentation | `cad/zeichnung/`, `cad/Grundplatte_V2.stp` |
| 21.11. | J | offen | Steckplan v2 für drei Ultraschallsensoren: alle Widerstände aufs Steckbrett, keine Kabelkreuzungen, Motorkabel in MDD3A-Reihenfolge | Hardware / Entscheidung | `elektronik/steckbrett_v2.png`, `elektronik/pinbelegung.md` |
| 23.11. | J | offen | Zweiter Haubendruck anprobiert, Frontsensor passte nicht. Front mit der Team-Baugruppe geprüft und geändert: Nasen-Rückwand weg, Fußschlitz höher | Fertigung / Konstruktion | `cad/haube_v4/` |
| 23.11. | J | offen | Zeichnung Grundplatte ergänzt (Durchmesser, t=5, Halbzeug, Oberfläche, Kanten), falsche Masse der Baugruppe gefunden | Konstruktion / Dokumentation | `cad/zeichnung/2026-11-23_Grundplatte_V3_Zeichnung.pdf` |
| 24.11. | J | offen | Ganzer Roboter als 3D-Modell ins Repo: STL zum Drehen auf GitHub, GLB mit Farben, STEP, sechs Ansichten | Konstruktion / Dokumentation | `cad/baugruppe/` |
| 24.11. | J | offen | Checkliste für die Abgabe von Dokumentation und Projektbericht: was gefordert ist, was fehlt | Organisation | `doku/abgabe_checkliste.md` |
| 24.11. | J | offen | Projektverlauf Woche für Woche (v0.6.0) und Darstellung der Projektergebnisse (v0.5.0) ins Repo, Checkliste danach aktualisiert | Dokumentation | `doku/ECHO-Projektverlauf-Wochen.pdf`, `doku/ECHO-Projektergebnisse.pdf` |
| 24.11. | offen | offen | Schaltplan v2 für den ganzen Roboter mit Notizen, mit dem Steckplan v2 verglichen | Elektronik / Dokumentation | `elektronik/schaltplan_v2.pdf` |

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

### KW 47

**17. bis 18.11.2026: Haube V4**
- Haubenentwürfe V1 bis V3 verworfen. V4 im Batmobil-/Panzer-Look: Echos mit Rohrblenden wie Waffen, Kotflügel mit Finnen, Heck nur als Anschlag für die Startwand
- Entscheidung: Freiraum-Regel bei der Haube ignorieren, Dach darf nah ans Podest, über dem MDD3A einige cm Kabelraum
- Entscheidung: Haube wird mit 7 × M3 × 16 durch die vorhandenen Plattenlöcher geschraubt, Mutter auf der anderen Seite, damit alles gerade sitzt
- Problem: Der Quarz auf der HC-SR04-Platine stieß an die Rohrblende. Lösung: Blende von 10,6 auf 8,4 mm gekürzt
- Problem: Die rechte Echo-Halterung stieß an den MDD3A und wurde 3,5 mm nach vorne versetzt. Die gedruckten Halterungen (`cad/stl/`) zeigen, dass auch die linke 1 mm anders sitzt. Lösung: Einschnitte links und rechts in der Haube einzeln angepasst, 0,5 mm Luft
- Problem: Die STEP-Datei kam in Creo nur als Flächen an (zu kleine Kanten und Ungenauigkeiten für Creo). Lösung: Geometrie bereinigt, jetzt eine STEP-Baugruppe mit echten Volumenkörpern
- Laut Prof darf die Haube mit KI erstellt werden, sie muss aber in Creo funktionieren
- Druck vorbereitet auf dem Bambu Lab X1E: ein Auftrag, Front und Heck stehen auf der Schnittkante, PLA, Baumstützen, Brim 8 mm
- Dateien und Anleitung: `cad/haube_v4/README.md`, Maße und Gründe: `cad/grundplatte-v2-entscheidungen.md`

**KW 47, bis 20.11.2026: Projektkarte, Projektverlauf, Marketing**
- Projektkarte mit Beschreibung, Inbetriebnahme, Erste Hilfe und Aufbau erstellt (`doku/ECHO-Projektkarte.pdf`). Offen: Foto des fertigen Roboters, Ablauf nach den letzten Tests prüfen, Rohrblenden nach dem Druck prüfen
- Dokumentation des Projektverlaufs nach der Vorlage aus Kap. 7 als Entwurf (heute `doku/ECHO-Projektverlauf-Wochen.docx`, zum Lesen als PDF daneben): Projektphasen, Teilergebnisse, Herausforderungen, Reflexion. Offen: Tests am Aufbau v2, Ergebnis von Abnahme und Abschlusspräsentation
- Marketing im eigenen Comic-Look: Cover „ECHO Nr. 1, der Roboter, der die Wand hört“ (A3 hoch) und Comic-Strip „ECHO und die Wand“ in 6 Bildern (A3 quer), in `doku/marketing/`. Offen: Ø-Tempo auf dem Cover, Uhrzeit und Raum der Live-Demo auf dem Strip

**20.11.2026: Haube anprobiert und geändert**
- Haube auf dem Bambu Lab X1E in einem Auftrag gedruckt und auf den Roboter gesetzt. Über den Rädern sitzt sie gut
- Problem: Die Wand im Radkasten berührte die Motorwelle und fast den Reifen. Gemessen: Räder innen 179,47 mm auseinander, außen 197,93 mm, Getriebe-Stirnseite 25,18 mm vor der Rad-Außenseite. Die Räder sitzen 7 mm weiter innen als in der Creo-Baugruppe
- Lösung: Wand am Rad ganz weg, Radkasten bis zur Platte offen. Reifen jetzt 6 mm zum Radlauf, Motor und Welle mindestens 19 mm
- Entscheidung: Teilung von x −15 auf x 58 verlegt, damit der ganze Kotflügel in einem Teil ist. Das Heck geht dafür nur noch ab, wenn die Schale ab ist. Keine USB-Öffnung für den ESP32
- Neue Dateien in `cad/haube_v4/`, Rohrblenden unverändert

**20.11.2026: Technische Zeichnung Grundplatte**
- Zeichnung BAT01.3.001.1 in Creo angelegt: A3, 1:1, Ordinatenbemaßung mit Nullpunkt an der Ecke oben links, dazu symmetrische Maße zur Mittellinie
- Rückmeldung vom Betreuer: Die Bemaßung ist so gut und bleibt. Nichts löschen, eine Koordinatentabelle mit x und y nur zusätzlich
- Im Modell alle Ø3,3 auf Ø3,2 gesetzt und 10 Löcher gelöscht, jetzt 37 Löcher (35 × Ø3,2, 2 × Ø2,2). STEP: `cad/Grundplatte_V3.stp` (seit 24.11. als Grundplatte V3 bezeichnet)
- Problem: In der ersten Fassung fehlten Durchmesser und Dicke, und es gab zwei verschiedene Nullpunkte für die senkrechten Maße. Lösung: ein Nullpunkt oben links, Rest am 23.11. ergänzt

**21.11.2026: Steckplan v2**
- Der erste Plan mit drei Ultraschallsensoren hatte die Spannungsteiler an den Sensoren und einen 10-kΩ-Pull-up am rechten Motor hängen. Neu geplant mit allen Widerständen auf dem Steckbrett (`elektronik/steckbrett_v2.png`)
- Echo vorne und rechts auf GPIO39 und GPIO36 (nur Eingang, reicht für Echo), Echo links auf GPIO4. Jeder Teiler hat denselben Aufbau: 1 kΩ, 2,2 kΩ zur blauen Schiene, Brücke zum Pin
- Encoder rechts von GPIO39 auf GPIO14 mit internem Pull-up, damit fällt der 10-kΩ-Widerstand weg. Grünes Encoder-Kabel wird nicht angeschlossen
- Echo vorne nicht mehr auf GPIO12, weil der ESP32 nicht startet, wenn GPIO12 beim Einschalten high ist
- Motor rechts hängt am MDD3A an M2. Die Motorkabel liegen am ESP32 jetzt in derselben Reihenfolge wie am MDD3A (M2B, M2A, M1B, M1A an 33, 32, 26, 25), so kreuzen sie sich nicht

### KW 48

**23.11.2026: Front der Haube angepasst**
- Haube mit Teilung bei x 58 gedruckt und aufgesetzt. Problem: Der vordere Ultraschallsensor passte nicht unter die Nase, die Front saß auf
- Ganze Baugruppe `batmobile-v2` als STEP aus Creo exportiert und die Haube gegen jedes Teil geprüft. Ursache: Der Stoßschalter reicht nach hinten bis x 136,8, die vorderen Schrauben vom Akkurahmen stehen bei x 140, y ±26 mit der Mutter oben auf der Platte. Genau dort stand die untere Rückwand der Nase
- Lösung: Rückwand der Nase entfernt (x 140 bis 142, bis z 20). Fußschlitz an den Seitenechos von z 4,5 auf 6,5 erhöht, weil die Schrauben der Echo-Halter bis z 5,1 hochstehen
- Danach gegen alle Teile der Baugruppe geprüft: keine Überschneidung. Am engsten sind die Klemmen vom MDD3A, 0,14 mm zur Flankenwand. Die Muttern von H1 bis H3 mit der flachen Seite an die Taschenwand legen
- Nur die Front muss neu gedruckt werden (70 g PLA), Heck und Rohrblenden bleiben. Neue Dateien in `cad/haube_v4/`

**23.11.2026: Zeichnung ergänzt, Masse der Baugruppe**
- Zeichnung ergänzt: „35x Ø3,2“ und „2x Ø2,2“, Dicke als „t=5“ statt Seitenansicht, Halbzeug „Sperrholzplatte 500x470x5“, Sammelangaben Oberfläche „lasergeschnitten“ und Kanten −0,5, kleine Isometrie 1:10 (`cad/zeichnung/2026-11-23_Grundplatte_V3_Zeichnung.pdf`)
- Entscheidung: keine Passungen und keine Abmaßtabelle. Die Löcher sind Durchgangslöcher für M3 und M2, die Allgemeintoleranz ISO 2768-m reicht
- Abgleich mit dem Modell: Die Ordinate x 236 (Kugelrolle) fehlt noch. Ein Podest-Loch sitzt im Modell bei x 56,0 statt 56,26, deshalb steht in der Zeichnung 142 statt 142,26
- Problem: Die Baugruppenzeichnung zeigt 10.823,294 kg. Der Parameter MASS wird per Beziehung aus dem Modell gerechnet, vermutlich haben Teile aus dem Internet kein Material und Creo nimmt die Standarddichte. Lösung offen: Masse zuweisen oder den Teilen Material geben. Creo lief danach nicht mehr, wird am 24.11. gemacht
- Creo meldet außerdem fehlende Referenzdateien SCHRAUBE_DIN_7991-M3X30 und M3X10 und 2 unterdrückte Komponenten in der Baugruppe

**24.11.2026: Gesamtmodell**
- Aus dem STEP-Export der Creo-Baugruppe vom 23.11. ein Gesamtmodell gemacht, damit man den fertigen Roboter ohne Creo sieht (`cad/baugruppe/`)
- Darin schon die Haubenfront vom 23.11. und die Räder an der gemessenen Stelle. Reifen zum Radlauf 5,3 bis 5,8 mm
- `ECHO_Roboter.stl` lässt sich auf GitHub im Browser drehen, `ECHO_Roboter.glb` hat Farben und geht in PowerPoint (Einfügen > 3D-Modelle), dazu die STEP-Datei als Zip und sechs Ansichten
- Beim Durchsehen aufgefallen: Im Export fehlen Steckbrett mit ESP32, Bedienpult und Schale. Die Motoren sind doppelt drin (JGA25-370 und Pololu 25D an derselben Stelle)

**24.11.2026: Checkliste für die Abgabe**
- Abgabe über Moodle: eine ZIP pro Gruppe mit README, Projekttagebüchern, Benutzerdoku, Entwicklerdoku, Projektverlauf, Creo-Baugruppe, Zeichnung des Chassis, Programmcode und Schalt- oder Verdrahtungsplan. Text-Dokumente nur als PDF
- Jede Anforderung mit dem Repo verglichen (`doku/abgabe_checkliste.md`). Ganz fehlen noch: README der ZIP, Entwicklerdokumentation, Programmablaufplan, native Creo-Dateien, Abschnitt „Wer hat was gemacht“ im Projektverlauf
- `main.py` hat noch die Pins vom 29.10., Zeichnung und Laserdatei passen bei der Lochzahl nicht zusammen (37 und 47)

**24.11.2026: Projektverlauf und Projektergebnisse**
- Projektverlauf neu aufgebaut, Woche für Woche mit Ziel, Erkenntnis, was gut lief und was besser ginge, dazu Zeitstrahl, Teilergebnisse, Abhängigkeiten und Gesamtfazit (`doku/ECHO-Projektverlauf-Wochen.docx`, ersetzt den Entwurf vom 19.11.)
- Darstellung der Projektergebnisse nach Vorlage Kap. 7: Benutzerdokumentation, Entwicklerdokumentation mit Programmablaufplan und Code Abschnitt für Abschnitt, bestehende Probleme, Weiterentwicklung (`doku/ECHO-Projektergebnisse.docx`)
- Projektkarte mit Bild aus dem 3D-Modell aktualisiert
- Beim Prüfen gegen die Abgabe aufgefallen: „Wer hat was gemacht“ fehlt im Projektverlauf, die Beschreibung der CAD-Entwürfe fehlt in der Entwicklerdoku, der Code-Teil beschreibt noch die Pins vom 29.10. Alles in `doku/abgabe_checkliste.md`

**24.11.2026: Schaltplan v2**
- Schaltplan für den ganzen Roboter: Akku über Wippschalter an VB+, MDD3A mit beiden Motoren, 5VO an 5 V, drei HC-SR04 mit Spannungsteiler, beide Encoder an 3,3 V, Stoßschalter an GPIO27 (`elektronik/schaltplan_v2.pdf`). Seite 2 erklärt jedes Teil und die Regeln für den Strom
- Mit dem Steckplan v2 verglichen: Motoren, Encoder, Stoßschalter, Trig-Pins und Echo vorne und rechts stimmen überein
- Problem: Echo links steht im Schaltplan an GPIO34, im Steckplan an GPIO4. Muss vor dem Umstecken entschieden werden

## Offene Punkte

- Code am neuen Roboter testen, Faktor für die Geradeausfahrt neu bestimmen (Gewicht und Aufbau haben sich geändert)
- Ultraschall und Bremsen auf dem neuen Aufbau nachtesten, Kipptest mit Ball
- Nach Steckplan v2 umstecken, Pins in `main.py` anpassen, Drehrichtung, Sensoren und Encoder einzeln testen
- Probedruck für die M3-Löcher, danach Halter drucken
- Akku-Wanne, Steckbrett-Halter und Taster mit größerem Kontaktpunkt modellieren
- Front der Haube (Stand 23.11.) neu drucken und am Roboter prüfen
- Creo-Baugruppe: Räder auf die Messung setzen (Reifen innen ±89,7 mm), Front der Haube gegen den Stand vom 23.11. tauschen, ein Motormodell entfernen, Steckbrett mit ESP32, Bedienpult und Schale ergänzen
- Schrauben für die Haube besorgen: 7 × M3 × 16, 7 Muttern M3, 11 Scheiben M3
- Schaltplan, Programmablaufplan und Creo-Baugruppe fertig machen
- Messen: Stößelspitze bis Plattenvorderkante, Motorlänge mit Encoder (Räder am 20.11. gemessen)
- Taster-Kabel: gewinkelte Steckhülsen oder Akku-Wanne verschieben
- Geschwindigkeit auf 200 cm messen (3 Mal)
- Beim Veranstalter klären: Podest unter der Schale, Wippschalter als Start, Sensoren an Start- und Endwand
- Projektkarte: Foto einfügen, Ablauf und Haube nach den Tests prüfen
- Projektverlauf: Tests am Aufbau v2 und Ergebnis der Abnahme ergänzen
- Comic: gemessenes Ø-Tempo auf dem Cover, Uhrzeit und Raum auf dem Strip eintragen
- Zeichnung Grundplatte fertig machen: Ordinate x 236 ergänzen, Maß 5 an der Isometrie löschen, „-0.5“ als „-0,5“, optional 8 durch Ordinate 248 ersetzen
- Podest-Loch im Modell von x 56,0 auf 56,26 korrigieren (Lochkreis Ø46)
- Klären: gelaserte Platte und DXF haben 47 Löcher, Modell und Zeichnung 37
- Masse der Baugruppe in Creo korrigieren (zeigt 10.823 kg), fehlende Schrauben SCHRAUBE_DIN_7991 einbinden
- Fehlende Zeiten und Kürzel in der Übersicht nachtragen
- Abgabe vorbereiten, alles Offene dafür steht in `doku/abgabe_checkliste.md`

## Wiedervorlagen

| Datum | Was |
| --- | --- |
| Fr 20.11.2026 | Fortschrittspräsentation KW 47 |
| Mi 25.11.2026 | Abnahmegespräch mit Demo |
| Fr 27.11.2026 | Abschlusspräsentation |
| bis Projektende | Abgabe als ZIP über Moodle, eine pro Gruppe (`doku/abgabe_checkliste.md`) |

## Zeitaufwand

Bisher nur aus dem Tagebuch von J übernommen. Bitte jeder seine Zeiten ab KW 45 ergänzen.

| Woche | Zeitraum | Zeit |
| --- | --- | --- |
| KW 42 | bis 16.10. | 2 h |
| KW 43 | 19. bis 23.10. | ca. 9 h 20 min |
| KW 44 | 26. bis 30.10. | ca. 7 h 10 min, ohne 29.10. vormittags und 30.10. |
| KW 45 | 02. bis 06.11. | ca. 2 h 10 min erfasst, Rest offen |
| KW 46 | 09. bis 13.11. | noch nicht erfasst |
| KW 47 | 16. bis 20.11. | noch nicht erfasst |
| KW 48 | ab 23.11. | noch nicht erfasst |
| Summe | | ca. 20 h 40 min erfasst |
