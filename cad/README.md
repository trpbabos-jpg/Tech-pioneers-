# CAD

- Creo-Teile (`.prt`) und die Baugruppe Roboter (`.asm`)
- Technische Zeichnung der Grundplatte als PDF (`zeichnung/`)
- DXF-Datei für den Lasercutter
- STL-Dateien der 3D-Druckteile (Halterungen, Podest, Haube)
- `baugruppe/`: der ganze Roboter als 3D-Modell (STL zum Drehen im Browser, GLB mit Farben, STEP) und Bilder
- `haube_v4/`: fertige Haube als STEP-Baugruppe für Creo und STL-Dateien zum Drucken
- `stl/`: gedruckte Echo-Halterungen links, rechts und vorne
- `skizzen/`: Formskizzen, z. B. die ECHO-Form in der Draufsicht vom 16.10. (Fledermaus-Ohren vorne, Umhang hinten, je ein Rad links und rechts)

Vor dem Hochladen in Creo alte Versionen aufräumen (Datei > Verwalten > Alte Versionen löschen), sonst landen `.prt.1`, `.prt.2` usw. im Repo.

## Was noch fehlt

Diese Dateien gibt es schon, sie liegen aber noch nicht im Repo. Bitte hochladen:

- Grundplatte v1 (Frankenstein-Modell): Creo-Dateien und Laser-Datei
- Creo-Dateien der Grundplatte v2, der Druckteile und der Baugruppe
- STL-Datei des Podests

## Gesamtmodell (Stand 24.11.2026)

`baugruppe/` zeigt den fertigen Roboter, erzeugt aus dem STEP-Export der Creo-Baugruppe vom 23.11. mit der Haubenfront vom 23.11. und den gemessenen Radpositionen. `baugruppe/ECHO_Roboter.stl` auf GitHub anklicken, dann lässt er sich im Browser drehen. Was dem Modell noch fehlt, steht in `baugruppe/README.md`.

## Baugruppe Roboter (Stand 13.11.2026)

Teilweise fertig, Screenshots in `../fotos/2026-11-13_cad_baugruppe/`. Enthalten: Grundplatte v2, Motoren mit Winkeln, Räder, Kugelrolle, MDD3A, Steckbrett mit ESP32, Podest für die Schale, drei Ultraschallsensoren mit Haltern. Es fehlen noch Haube, Akku mit Wanne, Bedienpult und Stoßfänger.

## Haube V4 (Stand 18.11.2026)

`haube_v4/Haube_V4.stp` in Creo als Baugruppe öffnen und in `roboter_v2` mit Default platzieren. Drucken, Montage und Prüfung: `haube_v4/README.md`.

## Echo-Halterungen

`stl/halterung-l-echo.stl`, `-r-echo.stl`, `-v-echo.stl`, so gedruckt. Alle drei haben denselben Körper, nur die Löcher sitzen anders: rechts 3,5 mm nach vorne versetzt (MDD3A), links 1 mm, vorne mittig mit 22,2 mm Lochabstand für den Stoßschalter.

## Grundplatte V2 (gelasert) und V3 (Modell)

Gelasert und verbaut ist die **V2** mit 47 Löchern. Am 20.11. wurden im Modell die zehn nicht gebrauchten Löcher gelöscht und alle Ø3,3 auf Ø3,2 gesetzt. Diesen Stand mit 37 Löchern nennen wir **V3**; er ist nicht gelasert.

- `Grundplatte_V2_Laser.dxf`: Laserdatei der V2, 1:1 in mm, nur Schnittlinien (256 × 170, 47 Löcher)
- `Grundplatte_V2_Laser.svg`: dieselbe Datei als SVG
- `Grundplatte_V3.stp`: Creo-Modell der V3 als STEP, Stand 20.11.2026 mit 37 Löchern (35 × Ø3,2, 2 × Ø2,2)
- `zeichnung/2026-11-23_Grundplatte_V3_Zeichnung.pdf`: technische Zeichnung BAT01.3.001.1 der V3, A3, 1:1. Bemaßung vom Betreuer abgenommen, ein paar Kleinigkeiten sind noch offen (Ordinate 236, Maß 5 an der Isometrie)
- Maßtabelle mit Lage, Schwerpunkt und Grenzwerten: `bom/Grundplatte_Masse_Gewicht_V2.xlsx`

Die Entscheidungen zur Grundplatte v2 stehen in `grundplatte-v2-entscheidungen.md`.

## Grundplatte v1 (Frankenstein-Modell)

- Platte 170 × 250 × 5 mm (Sperrholz Creative-Deco), Ecken R5, Ursprung hintere linke Ecke.
- Bohrungen mit Koordinatentabelle: 4 × Ø3,4 für die Pololu-Motorwinkel #2676 (je 2 Schrauben über Kreuz an den Randkerben, M3×12 Senkkopf von unten, Mutter oben) und 2 × Ø2,5 für die Stützkugel Pololu #955 (Lochabstand 15,5 mm, ohne Abstandshalter, Höhe passt zu 20,5 mm Bodenfreiheit).
- Laserwerte laut Testkarte Creative-Deco 5 mm: schneidet bei 5 mm/s ab 60 % und bei 7 mm/s ab 80 %.
