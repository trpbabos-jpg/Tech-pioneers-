# Änderungsverlauf

Die wichtigsten Schritte, Entscheidungen und Änderungen in zeitlicher Reihenfolge. Grundlage für die Dokumentation des Projektverlaufs. Details stehen im jeweiligen Ordner.

## KW 42

**16.10.2026: Pitch**
- Idee, Bauteilrecherche und Mind Map (`doku/mindmap_v1.pdf`, Miro-Board) vorgestellt
- Thema Batman: Ultraschall wie die Echoortung einer Fledermaus
- Folien: `doku/praesentationen/2026-10-16_pitch.pdf`, Datenblatt-Auszüge: `bom/datenblaetter/`
- Erste Formskizze ECHO: Differentialantrieb mit je einem Rad links und rechts, Stützkugel vorne (`cad/skizzen/2026-10-16_echo_form_draufsicht.png`)

**19.10.2026: erster Code**
- Testprogramme für Ultraschallsensor und Motor geschrieben

**20.10.2026: Steckbrett aufgebaut**
- ESP32, HC-SR04 mit Spannungsteiler und LED verkabelt, `ultraschall_test.py` läuft
- Motortreiber MDD3A und beide Motoren angeschlossen, Akku über Schalter
- Schaltplan und Kabelübersicht im Miro-Board angelegt
- Entscheidung: Sensor bekommt Strom über die Schienen, damit später mehr Sensoren dazukommen können
- Pinbelegung: `elektronik/pinbelegung.md`

## KW 43

**23.10.2026: Taster und Encoder**
- Taster an GPIO27, Encoder beider Motoren an 13, 14, 19 und 4
- GPIO18 verworfen, weil es ihn auf dem ESP32-PICO-V3 nicht gibt
- Pinwahl mit Herstellerunterlagen begründet (Folien: `doku/praesentationen/2026-10-23_encoder-pins.pdf`)
- Drehzahlmessung über die Encoder: 244 und 247 U/min (`doku/messwerte.md`)

## KW 44

**Ende Oktober: Frankenstein-Modell**
- Grundplatte v1 in Creo konstruiert und aus 5 mm Sperrholz gelasert, Motoren oben auf der Platte, Stützrad vorne
- Dient als fahrtüchtiger Prototyp für Encoder-Tests und Kalibrierung
- Folien vom 30.10.: `doku/praesentationen/2026-10-30_frankenstein-modell-und-encoder.pdf`

**29.10.2026: neu verkabelt und kalibriert**
- Steckbrett komplett neu belegt, damit sich keine Kabel kreuzen (`elektronik/pinbelegung.md`)
- Fehler gefunden: Räder drehten gegeneinander, Ursache war die Verkabelung, behoben über `RICHTUNG_RECHTS`
- Kalibrierung: Anlauf 20 %, Faktor links 0,94 (`code/einstellwerte.md`)
- Erste Fahrt auf dem Boden mit sanftem Bremsen, Stopp bei 13,1 cm

**30.10.2026: main.py vereinfacht**
- Statt der Zustände nur noch drei Schritte: hinfahren, sanft bremsen bis der Stoßschalter auslöst, rückwärts dieselbe Strecke zurück
- Ultraschall über den Median der letzten 3 Messungen
- Erkenntnis: Der Ultraschall sitzt ca. 10 cm hinter dem Stoßschalter, deshalb Bremsbeginn später auf 45 bis 50 cm
- Code: `code/fahren_v2_vereinfacht.py`

## KW 45

**03.11.2026: schneller fahren, Korrektur abhängig vom Tempo**
- Erst VMAX 100 ausprobiert (`code/fahren_v3_vmax100.py`), dann VMAX 80 und Kriechen 20 %
- Beim Kriechen an der Wand fuhr er schief, weil die Korrektur von ±8 % bei 20 % zu stark war. Jetzt wird die Grenze mit dem Tempo kleiner
- Eigener Faktor links für die Rückfahrt (`FAKTOR_LINKS_ZURUECK`)
- Faktor links auf 0,7 gesetzt, gleicht die Mechanik aus, wird mit der Grundplatte v2 neu bestimmt
- Aktueller Stand: `code/main.py`, Werte in `code/einstellwerte.md`

**Anfang November: main.py erweitert**
- Ablauf: Hinfahrt, sanft bremsen, Wand mit Stoßschalter berühren, rückwärts über die Encoder zur Startwand (ohne Wenden)
- Stoßschalter löste beim Fahren fälschlich aus, Entprellung eingebaut
- Test mit gestapelten Stühlen als Wand: Ultraschall misst unruhig, weil die Wand uneben ist, nicht wegen des Codes

**05.11.2026: Grundplatte v2 geplant**
- Maßtabelle mit allen Bauteilen, Gewichten und offenen Maßen angelegt

**06.11.2026: Entscheidungen Grundplatte v2**
- Variante B „Turm“: Schale auf gedrucktem Podest über dem Schwerpunkt (`cad/grundplatte-v2-entscheidungen.md`)
- Kein Klett mehr, alle Halterungen 3D-gedruckt und mit M3 verschraubt
- Drei Ultraschallsensoren statt einem, weil die Seitenwände nicht gerade sind
- Wippschalter wird Hauptschalter und Startknopf
- Team ist jetzt zu viert, Planung mit Kanban und Zeitplan im Miro-Board, dieses Repository angelegt
- Weekly Closing KW 45: `doku/praesentationen/2026-11-06_weekly-closing-kw45.pdf` (die drei Testvideos sind im PDF nur als Standbild)

**06.11.2026: Grundplatte v2 fertig zum Lasern**
- Rückwand gestrichen, das Heck der Batmobil-Haube wird die Anlagefläche an der Startwand
- 7 Löcher für die Haube, MDD3A direkt mit 4 × M3 auf Abstandshülsen, keine Langlöcher mehr
- Laserdatei, Zeichnung und Maßtabelle hochgeladen (`cad/`, `bom/`)
- Vor dem Lasern noch messen: Lochbild MDD3A, Abstand Schalterloch bis Stößelspitze, Plattendicke

## KW 46

**09.11.2026: Grundplatte v2 gelasert**
- Platte aus 5 mm Sperrholz gelasert, alle Löcher passen
- Motoren, Räder, Kugelrolle, MDD3A und Stoßschalter werden direkt auf die Platte geschraubt
- Nächster Schritt: Steckbrett-Wanne, Akku-Wanne und Bedienpult in Creo zeichnen und drucken

**09.11.2026: erster Aufbau auf der Grundplatte v2**
- Motoren, Kugelrolle, MDD3A, Stoßschalter und Akku probeweise aufgebaut (Fotos in `fotos/`, 09.11.)
- Problem: Die M2-Schrauben der Kugelrolle stehen oben über, der Stoßschalter lag darauf und kippte nach vorne. Umdrehen ging nicht, weil die Schrauben dann die Kugel berühren
- Lösung: unter beide Schrauben des Stoßschalters je zwei M3-Muttern gestapelt, er steht jetzt gerade ca. 5 mm höher
- Problem: Der Stoßschalter ist mit Flachsteckhülsen 50 bis 55 mm lang und kommt der Akku-Wanne in die Quere. Lösung offen: gewinkelte Steckhülsen oder Akku-Wanne bis 8 mm nach hinten
- Idee: Die zwei langen M3-Schrauben des Stoßschalters tragen gleich den Halter für den vorderen Ultraschallsensor. Die zwei Pfosten fallen weg, die Löcher bei x 163 bleiben frei
- Noch messen: Abstand Stößelspitze bis Plattenvorderkante, danach Stoßfänger mit Finger zum Stößel drucken


**13.11.2026: Echo-Halterung, Verkabelung, CAD-Baugruppe**
- Echo-Halterung für den vorderen Ultraschallsensor gedruckt und montiert, sie sitzt auf den Schrauben des Stoßschalters
- Elektronik auf der Grundplatte v2 komplett verkabelt (Foto: `fotos/2026-11-13_elektronik_verkabelt.jpg`)
- CAD-Baugruppe des Roboters in Creo teilweise fertig: Grundplatte v2, Motoren mit Winkeln, Räder, Kugelrolle, MDD3A, Steckbrett mit ESP32, Podest für die Schale, drei Ultraschallsensoren mit Haltern (vorne über dem Stoßschalter, links und rechts). Screenshots in `cad/screenshots/`
- Noch nicht in der Baugruppe: Haube, Akku mit Wanne, Bedienpult mit Wippschalter, Stoßfänger
