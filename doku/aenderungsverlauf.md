# Änderungsverlauf

Die wichtigsten Schritte, Entscheidungen und Änderungen in zeitlicher Reihenfolge. Grundlage für die Dokumentation des Projektverlaufs. Details stehen im jeweiligen Ordner.

## KW 42

**16.10.2026: Pitch**
- Idee, Bauteilrecherche und Mind Map (`doku/mindmap_v1.pdf`, Miro-Board) vorgestellt
- Thema Batman: Ultraschall wie die Echoortung einer Fledermaus

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
- Pinwahl mit Herstellerunterlagen begründet
- Drehzahlmessung über die Encoder: 244 und 247 U/min (`doku/messwerte.md`)

## KW 44

**Ende Oktober: Frankenstein-Modell**
- Grundplatte v1 in Creo konstruiert und aus 5 mm Sperrholz gelasert, Motoren oben auf der Platte, Stützrad vorne
- Dient als fahrtüchtiger Prototyp für Encoder-Tests und Kalibrierung

**29.10.2026: neu verkabelt und kalibriert**
- Steckbrett komplett neu belegt, damit sich keine Kabel kreuzen (`elektronik/pinbelegung.md`)
- Fehler gefunden: Räder drehten gegeneinander, Ursache war die Verkabelung, behoben über `RICHTUNG_RECHTS`
- Kalibrierung: Anlauf 20 %, Faktor links 0,94 (`code/einstellwerte.md`)
- Erste Fahrt auf dem Boden mit sanftem Bremsen, Stopp bei 13,1 cm

## KW 45

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
