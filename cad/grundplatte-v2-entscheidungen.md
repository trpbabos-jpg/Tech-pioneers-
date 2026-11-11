# Grundplatte V2: Entscheidungen und Hauptmaße (Stand 06.11.2026)

Koordinaten: Ursprung = Mitte Radachse auf Plattenoberseite, x vorne, y links, z hoch. Plattenoberseite 25,5 mm über Boden.
Maßgrundlage ist die Excel des Teams (Grundplatte_Masse_Gewicht). PDF der Variante A und Schalen-STL werden nicht gebraucht.

## Entscheidung
- Variante B "Turm": Schale auf gedrucktem Podest über dem Schwerpunkt, alles andere flach darunter.
- Variante C (Schale vorne, Räder außerhalb des Freiraum-Kreises, Rand ca. 78 mm) verworfen: Roboter starr, tiefere Schale bringt dem Ball nichts, Roboter wird länger, Schale weit vor dem Schwerpunkt.
- Variante A des Teams anhand der Problemliste bewertet.
- 06.11.: Rückwand und Zapfen gestrichen. Das Heck der Batmobil-Haube übernimmt die Anlage an der Startwand.
- 06.11.: MDD3A ohne Druckteil direkt auf die Platte (4 × M3, Abstandshülsen 5 mm).
- 09.11.: Stoßschalter auf je zwei M3-Muttern unterlegt, weil die Kugelrollen-Schrauben oben überstehen. Frontsensor-Halter sitzt auf den zwei Schrauben des Stoßschalters statt auf eigenen Pfosten.
- 06.11.: Keine Langlöcher mehr. Stoßschalter mit 2 runden M3-Löchern, Schaltpunkt wird am gedruckten Bügel eingestellt.

## Freiraum (Regel 4)
- Schalenrand 105 mm über Boden (Räder 80 + 20 + 5 Reserve). Freiraum gilt ab 85 mm, Kreis Ø262.
- Alles außer Podest und Schale bleibt unter 85 mm über Boden (59,5 über Plattenoberseite).
- Podest oberhalb 85 mm nur Rohr Ø36 und Kopf Ø62, ganz unter der Schale Ø102 verdeckt. Lesart beim Veranstalter bestätigen.

## Schale (laut Excel)
- Ø102 am Rand, Nabe Ø43,2 mit 6 Laschen zum Verschrauben, 26 g mit Ball.
- Podest-Kopf Ø62 × 4 mit Mulde Ø43,6 × 2 und 6 Löchern für die Laschen, 45°-Fase darunter. Kopf-Oberkante über Platte = 81,5 − Schalenhöhe (2 mm Mulde für die Nabe eingerechnet), bei 12,3 also 69,2. Skizze: `skizzen/2026-11-11_podest_schnitt.png`.
- Noch messen: Gesamthöhe der Schale, Lochkreis und Loch-Ø der Laschen.

## Start und Strom
- Startknopf ist der Wippschalter (Hauptschalter) zwischen Akku und MDD3A. Vom MDD3A 5VO geht ein Kabel zur roten Schiene des Steckbretts.
- Wippschalter oben im Bedienpult links neben dem Podest (Ausschnitt 27,2 × 12,2 bei x 38, y 60).
- Code: nach dem Booten 3 s warten, dann losfahren (Regel: 2 bis 10 s an der Startwand).
- 5VO laut Cytron-Datenblatt max. 200 mA, WLAN aus lassen.
- Beim Veranstalter fragen, ob der Wippschalter als Startknopf zählt. Ersatz: Stoßschalter vorne als Start.

## Platte
- Sperrholz 5 mm, 256 × 170 (x −86 bis +170, y ±85), Ecken R8, gerade Hinterkante. Ca. 153 g. 47 runde Löcher.
- Hinten 10 mm freier Streifen (x −86 bis −76) hinter der Steckbrett-Wanne für die Haubenschrauben.
- Motorwinkel wie V1: Löcher x ±10,85, |y| 76,5 und 44,75.
- Podest 4 × M3 auf LK Ø46 um (40, 0). Kugelrolle 2 × M2 bei (150, ±7,75).
- MDD3A 4 × M3 bei x 19,25 / 61,25 und y −34,5 / −71,5 (Lochbild 42 × 37 aus Foto, vor dem Lasern messen).
- Stoßschalter 2 × M3 bei (160, ±11,1), Lochabstand 22,2.
- Haube 7 × M3: H1 bis H3 (−81 / 60, 0, −60), H4/H5 (130 / ±78), H6/H7 (162 / ±45). Schrauben von unten in Gewindeeinsätze M3 in Domen Ø8.
- M3 gezeichnet Ø3,2, M2 Ø2,2.

## Haube (Batmobil)
- Im Freiraum-Kreis höchstens 85 mm über Boden. Höher nur an den Heckecken (x < −60 am Rand) und vorne vor x 171.
- Heck eben bei x ≤ −88, ca. 10 bis 70 mm über Boden, 3 mm Wand mit Rippen, fest verschraubt.
- Löcher Ø19 bis 20 für die Ultraschallkapseln (Kapsel bündig, kein Kontakt), Öffnung über dem Wippschalter, Loch Ø64 für das Podest, USB-Öffnung, Stoßfänger frei.
- Neben den Rädern innerhalb ±86 oder Kotflügel. Druck in zwei Hälften, Teilung etwa bei x 60.

## Anordnung
- Hinten quer: Steckbrett + ESP32 in Druckwanne (x −76 bis −21,1). Mitte: Motoren, Podest (x 40), links Bedienpult mit Wippschalter, rechts MDD3A.
- Vorne: Akku (Trimmgewicht), Kugelrolle, Frontsensor, Stoßschalter, federnder Bügel (Mitte x 182 bei 17,6 mm von Schalterloch bis Stößelspitze).
- Seitensensoren x 66 bis 112 auf Abstandshaltern, Kapseln 3 mm über dem Plattenrand, Kapselmitte 50 mm über Boden.

## Rechenwerte
- Masse ca. 850 g ohne Haube, Schwerpunkt x 41, y 0, 37 mm über Boden.
- Ball: Startwert a_max 0,3 m/s², Rampe 0,3 s, Kriechen 0,05 m/s an der Endwand, Pause 1 s. Nach Kipptest ggf. bis 0,8.

## Offen
- Schalenhöhe und Laschen-Lochkreis, Motorlänge mit Encoder, Spurweite, Akkuhöhe, MDD3A-Lochbild, Abstand Schalterloch bis Stößelspitze, Plattendicke, Masse der Haube.
- Beim Veranstalter: Podest-Lesart, Wippschalter als Start, Sensoren an Start- und Endwand.
