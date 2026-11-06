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

## Grundplatte v2

- `Grundplatte_V2_Laser.dxf`: Laserdatei, 1:1 in mm, nur Schnittlinien (256 × 170, 47 Löcher)
- `Grundplatte_V2_Laser.svg`: dieselbe Datei als SVG
- `Grundplatte_V2_Zeichnung_A3.pdf`: 3 Blätter A3 1:1, Draufsicht mit Bohrungstabelle, Seitenansicht mit Freiraum und Regeln für die Haube, Anordnung der Bauteile
- Maßtabelle mit Lage, Schwerpunkt und Grenzwerten: `bom/Grundplatte_Masse_Gewicht_V2.xlsx`

Die Entscheidungen zur Grundplatte v2 stehen in `grundplatte-v2-entscheidungen.md`.
