# Haube V4 (Stand 18.11.2026)

Fertige Haube für ECHO: Batmobil-/Panzer-Look, die Echos schauen wie Waffen aus der Haube. Die Haube darf laut Prof mit KI erstellt werden, muss aber in Creo funktionieren. Deshalb gibt es sie als STEP-Baugruppe mit echten Volumenkörpern.

| Datei | Wofür |
| --- | --- |
| `Haube_V4.stp` | Creo. STEP-Baugruppe HAUBE_V4 mit HAUBE_HECK, HAUBE_FRONT und ROHRBLENDE (dreimal verbaut: links, rechts, vorne) |
| `Haube_V4_Heck.stl` | Druck, Heckteil (ESP32 und Steckbrett darunter) |
| `Haube_V4_Front.stl` | Druck, Frontteil |
| `Rohrblende_3x.stl` | Druck, dreimal drucken |
| `Einschnitte_links_rechts.png` | So sitzen Halterung, Rohrblende und Haube an den Seitenechos |

## In Creo

1. Datei > Öffnen, Typ STEP, `Haube_V4.stp`. Im Fenster „Import New Model“ Type **Assembly** wählen.
2. Kontrolle: Teil öffnen, Analysis > Mass Properties. Steht ein Volumen da, ist es ein Volumenkörper (Heck ca. 98 900 mm³).
3. In jedem Teil Material anlegen: File > Prepare > Model Properties > Material > change > File > New. PLA, Density 1,24 g/cm³.
4. In `roboter_v2` über Assemble `haube_v4.asm` einfügen und mit **Default** platzieren. Die Koordinaten sind wie in der Baugruppe: Ursprung Achsmitte auf der Plattenoberseite, Creo X nach vorne, Creo Y nach oben.

Masse in PLA: Heck 123 g, Front 147 g, Rohrblende je 4,9 g.

## Drucken (Bambu Lab X1E)

Front und Heck passen flach nicht zusammen aufs Bett (263 mm, Bett 256). Für einen einzigen Druckauftrag stehen beide auf ihrer Schnittkante (x −15): Front mit der Nase nach oben, Heck mit dem Anschlag nach oben. Rohrblenden flach auf der Rückseite.

- Filament PLA Basic für Teile und Stützen
- 0,20 mm Standard, 15 % Füllung, 2 Wandlinien
- Stützen: Baum (auto), nur auf Druckplatte
- Brim „nur außen“, 8 mm für Front und Heck. Für die Rohrblenden kein Brim (Objekteinstellung)
- Schraublöcher nach dem Druck mit 3,5 mm aufbohren

## Montage

1. Schale vom Podest nehmen (Dachloch Ø66 muss über den Podestkopf Ø62).
2. Rohrblenden auf die Kapseln der drei Ultraschallsensoren stecken (Klemmsitz).
3. Front von oben aufsetzen, H4 bis H7 verschrauben.
4. Muttern in die Taschen von H1 bis H3 legen (Klebeband), Heck aufsetzen, verschrauben.

Schrauben: 7 × M3 × 16 von unten durch die Platte, Scheibe unter dem Kopf, oben bzw. in der Tasche Mutter M3. Zum Code-Ändern nur H1 bis H3 lösen und das Heck abheben.

## Geprüft

Mit allen Bauteilen der Baugruppe und den echten Halterungen (`../stl/halterung-*-echo.stl`, Abweichung unter 0,01 mm nachgebaut):

- keine Überschneidung
- Rohrblende zur Haube 0,5 mm, Halterungen zur Haube 0,5 mm (vorne 2 mm), MDD3A 0,5 mm, Bedienpult 1,1 mm
- Plattenkante 0,3 mm Luft, passt auch bei 0,2 mm größerer Platte
- Schallkegel (±15° ab Kapselspitze) frei, mindestens 0,57 mm
- beide Teile lassen sich senkrecht von oben aufsetzen, nur die Schale muss vorher ab
- STEP: jedes Teil ein geschlossener Körper, Toleranz 1e-7 mm, kürzeste Kante 0,78 mm (Creo braucht hier über ca. 0,4 mm, sonst kommen nur Flächen an)

Herleitung, Maße und Entscheidungen: `../grundplatte-v2-entscheidungen.md`. Die Schritt-für-Schritt-Anleitung zum Nachbauen in Creo liegt als eigenes Dokument „Creo-Anleitung Haube V4“ vor, die Abweichungen der fertigen Datei stehen dort oben.
