# Kaufteile: CAD-Modelle für die Baugruppe Roboter

Woher wir die 3D-Modelle der Kaufteile für die Creo-Baugruppe nehmen. Die Bauteile stehen in `bom/materialliste.md`. STEP-Dateien in Creo über Datei > Öffnen importieren und als `.prt` speichern.

Heruntergeladene STEP-Dateien bitte in `cad/kaufteile/` ablegen, Dateiname wie in der Spalte „Datei“.

## Offizielle Herstellerdateien

| Bauteil | Anzahl | Quelle | Datei |
| --- | --- | --- | --- |
| Motorhalterung Pololu #2676 (25D) | 2 | https://www.pololu.com/product/2676/resources | `pololu_2676_motorhalterung.step` |
| Stützkugel Pololu #955 (3/4″ Metallkugel) | 1 | https://www.pololu.com/product/955/resources | `pololu_955_stuetzkugel.step` |
| Rad 80 × 10 mm | 2 | https://www.pololu.com/product/1430/resources (Zip mit STEP) | `pololu_rad_80x10.step` |
| Motortreiber Cytron MDD3A | 1 | Produktseite MDD3A auf cytron.io, „3D CAD files (Zip)“ | `cytron_mdd3a.step` |

## Community-Modelle (GrabCAD, kostenloser Account nötig)

| Bauteil | Anzahl | Quelle | Datei |
| --- | --- | --- | --- |
| Motor DFRobot FIT0520 | 2 | https://grabcad.com/library/jga25-370-2 (baugleicher 25-mm-Getriebemotor) | `motor_fit0520.step` |
| ESP32-PICO-KIT | 1 | GrabCAD-Suche „ESP32-PICO-KIT“ oder SnapEDA (ESP32-PICO-KIT) | `esp32_pico_kit.step` |
| Ultraschallsensor HC-SR04 | 3 | GrabCAD-Suche „HC-SR04“ | `hc-sr04.step` |
| Steckbrett | 1 | GrabCAD-Suche „breadboard“, Größe mit unserem vergleichen | `steckbrett.step` |
| Akkuhalter 4 × AA | 1 | GrabCAD-Suche „4xAA battery holder“ | `akkuhalter_4xaa.step` |

## Selbst modellieren

| Bauteil | Anzahl | Vorgehen |
| --- | --- | --- |
| Wippschalter Marquardt 01552.3102-00 | 1 | Keine freie STEP gefunden. Vereinfacht nach Datenblatt: Gehäuse-Quader, Rahmen, Wippe |
| Stoßschalter Marquardt 01115.2101-02 | 1 | Wie oben, Maße am Bauteil nachmessen |
| Akku Eneloop AA | 4 | Zylinder Ø 14,5 × 50,5 mm |
| Tischtennisball | 1 | Kugel Ø 40 mm |
| Schrauben M3 und M2, Muttern, Scheiben | | Creo-Normteile oder STEP von TraceParts |
| Abstandshülse M3 × 5 mm | 4 | Zylinder mit Bohrung, Maße nachmessen |
| Gewindeeinsatz M3 | 7 | Vereinfacht als Zylinder, Maße nachmessen |

Eigene Teile (Grundplatte, Podest, Haube, Steckbrett-Wanne, Halterungen) haben wir schon in Creo, siehe `cad/README.md`.

## Worauf achten

- **Motor:** DFRobot stellt für den FIT0520 kein CAD-Modell bereit. Laut DFRobot-Wiki misst er 50 × Ø 24,4 mm. Das JGA25-370-Modell kommt dem nahe. Länge, Wellenlänge (D-Welle 4 mm) und Encoder-Deckel an unserem Motor nachmessen und das Modell bei Bedarf anpassen.
- **Räder:** Unsere Räder sind sehr wahrscheinlich die Pololu Multi-Hub-Räder (#3690/#3691) mit Spannzangen für 3- und 4-mm-Wellen. Dafür gibt es nur eine Maßzeichnung, keine STEP. Wir nehmen deshalb die STEP vom normalen 80 × 10-mm-Rad, die Außenmaße sind gleich.
- **ESP32:** In der Materialliste steht „ESP32-PICO-KIT V1“. Die Modelle bei GrabCAD und SnapEDA sind das ESP32-PICO-KIT (V4). Länge, Breite und Pinanzahl mit unserem Board vergleichen.
- **Allgemein:** Community-Modelle sind nicht vom Hersteller. Vor dem Einbau immer die wichtigsten Maße (Außenmaße, Lochabstände) mit dem echten Bauteil vergleichen.

## Tipp für die Baugruppe

1. Grundplatte als erstes Teil mit Standard-Platzierung einfügen.
2. Alle anderen Teile über die Bohrungen einbauen: Achse auf Achse und Fläche auf Fläche.
3. So sitzen die Teile automatisch richtig, wenn die Lochpositionen in der Grundplatte stimmen. Passt etwas nicht, ist das ein Hinweis auf einen Fehler in der Grundplatte.
