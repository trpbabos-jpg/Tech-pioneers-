# CAD

- Creo-Teile (`.prt`) und die Baugruppe Roboter (`.asm`)
- Technische Zeichnung der Grundplatte als PDF
- DXF-Datei für den Lasercutter
- STL-Dateien der 3D-Druckteile (Halterungen, Podest, Haube)
- `skizzen/`: Formskizzen, z. B. die ECHO-Form in der Draufsicht vom 16.10. (Fledermaus-Ohren vorne, Umhang hinten, je ein Rad links und rechts)

Vor dem Hochladen in Creo alte Versionen aufräumen (Datei > Verwalten > Alte Versionen löschen), sonst landen `.prt.1`, `.prt.2` usw. im Repo.

## Was noch fehlt

Diese Dateien gibt es schon, sie liegen aber noch nicht im Repo. Bitte hochladen:

- Grundplatte v1 (Frankenstein-Modell): Creo-Dateien und Laser-Datei
- Creo-Dateien der Grundplatte v2, der Druckteile und der Baugruppe
- STL-Dateien der Druckteile

## Baugruppe Roboter (Stand 13.11.2026)

Teilweise fertig, Screenshots in `../fotos/2026-11-13_cad_baugruppe/`. Enthalten: Grundplatte v2, Motoren mit Winkeln, Räder, Kugelrolle, MDD3A, Steckbrett mit ESP32, Podest für die Schale, drei Ultraschallsensoren mit Haltern. Es fehlen noch Haube, Akku mit Wanne, Bedienpult und Stoßfänger.

## Grundplatte v2

- `Grundplatte_V2_Laser.dxf`: Laserdatei, 1:1 in mm, nur Schnittlinien (256 × 170, 47 Löcher)
- `Grundplatte_V2_Laser.svg`: dieselbe Datei als SVG
- Maßtabelle mit Lage, Schwerpunkt und Grenzwerten: `bom/Grundplatte_Masse_Gewicht_V2.xlsx`

Die Entscheidungen zur Grundplatte v2 stehen in `grundplatte-v2-entscheidungen.md`.

## Grundplatte v1 (Frankenstein-Modell)

- Platte 170 × 250 × 5 mm (Sperrholz Creative-Deco), Ecken R5, Ursprung hintere linke Ecke.
- Bohrungen mit Koordinatentabelle: 4 × Ø3,4 für die Pololu-Motorwinkel #2676 (je 2 Schrauben über Kreuz an den Randkerben, M3×12 Senkkopf von unten, Mutter oben) und 2 × Ø2,5 für die Stützkugel Pololu #955 (Lochabstand 15,5 mm, ohne Abstandshalter, Höhe passt zu 20,5 mm Bodenfreiheit).
- Laserwerte laut Testkarte Creative-Deco 5 mm: schneidet bei 5 mm/s ab 60 % und bei 7 mm/s ab 80 %.
