# Grundplatte V2: Entscheidungen und Hauptmaße (Stand 23.11.2026)

Koordinaten: Ursprung = Mitte Radachse auf Plattenoberseite, x vorne, y links, z hoch. Plattenoberseite 25,5 mm über Boden.
Maßgrundlage ist die Excel des Teams (`bom/Grundplatte_Masse_Gewicht_V2.xlsx`), die Teileliste vom 17.11. (Sensor-Aufsatz, Seitenhalter, Tasteraufsatz, Akku-Schienen-Rahmen) die gedruckten Echo-Halterungen (`cad/stl/halterung-*-echo.stl`), die Radmessung vom 20.11. und die Team-Baugruppe `batmobile-v2` (STEP vom 23.11.; dort Creo X = x, Creo Y = z + 5, Creo Z = −y).
Fertige Haube: `cad/haube_v4/`. Creo-Anleitungen als eigene Dokumente: „Creo-Anleitung Grundplatte V2“, „Creo-Anleitung Haube V4“ (28 Schritte plus Rohrblende), „Creo-Anleitung Haube V1“ (überholt) und „Grundplatte BAT01.3.001.1, Zeichnung in Creo 13 Schritt für Schritt“.

## Entscheidung
- Variante B „Turm“: Schale auf gedrucktem Podest über dem Schwerpunkt, alles andere flach darunter.
- Variante C (Schale vorne, Räder außerhalb des Freiraum-Kreises, Rand ca. 78 mm) verworfen: Roboter starr, tiefere Schale bringt dem Ball nichts, Roboter wird länger, Schale weit vor dem Schwerpunkt.
- Variante A des Teams anhand der Problemliste bewertet.
- 06.11.: Rückwand und Zapfen gestrichen. Das Heck der Haube übernimmt die Anlage an der Startwand.
- 06.11.: MDD3A ohne Druckteil direkt auf die Platte (4 × M3, Abstandshülsen 5 mm).
- 06.11.: Keine Langlöcher mehr. Stoßschalter mit 2 runden M3-Löchern, Schaltpunkt wird am gedruckten Bügel eingestellt.
- 17.11.: Freiraum-Regel wird bei der Haube bewusst ignoriert (Wunsch des Teams).
- 18.11.: Haube wird durchgeschraubt: Schraube M3 durch Platte und Haube, auf der anderen Seite Mutter, damit alles gerade sitzt. Ersetzt die Ideen vom 17.11. (Einschmelzmuttern, Stifte, selbstschneidend in PLA).
- 18.11.: Haube V4 vom Team freigegeben.
- 18.11.: Rohrblende von 10,6 auf 8,4 mm Tiefe gekürzt. Grund: Der Quarz (silbern, HC-49/S) auf der Vorderseite der HC-SR04-Platine steht 3,4 mm hoch, die Blende stieß dagegen.
- 18.11.: Rechte Echo-Halterung um 3,5 mm nach vorne verschoben, weil sie gegen den MDD3A stieß. Haube: Echo-Einschnitt rechts mit eigener Skizze statt gespiegelt.
- 18.11.: Laut Prof muss die Haube nicht selbst modelliert werden, sie darf mit KI erstellt werden, muss aber in Creo funktionieren. Deshalb fertige STEP-Baugruppe `Haube_V4.stp` mit echten Volumenkörpern. Die ersten STEPs kamen in Creo nur als Flächen an (eine Kante mit 0,2 mm Toleranz, zwei 0,16-mm-Kanten; Creo rechnet bei dieser Teilgröße mit etwa 0,3 bis 0,4 mm Genauigkeit).
- 18.11.: Grundplatte ist in echt 1:1 wie das Modell, die drei Echo-Halterungen sind 1:1 nach den STLs gedruckt. Danach linke Halterung und linker Einschnitt korrigiert, 0,3 mm Luft zur Plattenkante eingebaut.
- 18.11.: Gedruckt wird in einem Auftrag auf dem Bambu Lab X1E: Front und Heck stehen auf ihrer Schnittkante, Rohrblenden flach.
- 20.11.: Erster Druck am Roboter anprobiert: Die Flankenwand im Radkasten berührte die Motorwelle und fast den Reifen. Gemessen: Räder innen 179,47 auseinander, außen 197,93, Getriebe-Stirnseite 25,18 vor der Rad-Außenseite. Die Räder sitzen also bei y ±89,7 bis ±99,0, nicht bei ±97 bis ±107 wie in der Creo-Baugruppe. Lösung: Wand am Rad ganz weg, Radkasten bis zur Platte offen.
- 20.11.: Neue Teilung bei x 58, damit der ganze Kotflügel in einem Teil ist. Heck = alles bis zur Kotflügel-Vorderkante, Front = Echo-Einschnitte und Nase. Folge: Das Podestloch ist geteilt, das Heck geht nur ab, wenn die Schale ab ist. Eine USB-Öffnung für den ESP32 ist nicht gewünscht.
- 23.11.: Zweiter Druck am Roboter: Der Frontsensor passte nicht, die Nase saß auf. Ursache laut Team-Baugruppe: Der Stoßschalter (Marquardt 1115.2101) reicht nach hinten bis x 136,8, die vorderen Akkurahmen-Schrauben stehen bei (140, ±26) mit Mutter oben auf der Platte. Darauf stand die untere Rückwand der Nase (x 140 bis 142, bis z 20). Lösung: Rückwand entfernt (|y| < 66, z < 20). Dazu Fußschlitz der Echo-Einschnitte von z 4,5 auf 6,5 erhöht, weil die Schrauben der Echo-Halter laut Baugruppe bis z 5,1 hochstehen. Nur die Front ändert sich, Heck und Rohrblenden bleiben.
- 20.11.: Im Creo-Modell alle Ø3,3 auf Ø3,2 vereinheitlicht und 10 Löcher gelöscht: (−62 / ±55), (−35 / ±55), (148 / ±70), (160 / ±70), (163 / ±28). Modell jetzt 37 Löcher.

## Technische Zeichnung (BAT01.3.001.1)
- 20.11.: Ordinatenbemaßung mit Nullpunkt an der Ecke oben links in der Zeichnung (hinten links an der Platte), waagerecht ab der linken Kante, senkrecht ab der oberen Kante. Zusätzlich symmetrische Maße zur Mittellinie (rechts 15,5 bis 156, links 32,52).
- 20.11.: Laut Betreuer ist die Bemaßung so gut und bleibt. Nichts löschen, eine Koordinatentabelle mit x und y nur zusätzlich.
- 23.11.: Durchmesser als Hinweis „35x Ø3,2“ und „2x Ø2,2“.
- 23.11.: Dicke als „t=5“ in der Platte (ISO 3898, Kap. 4.4), dafür keine Seitenansicht. Kleine Isometrie 1:10 daneben.
- 23.11.: Keine Passungen. Ø3,2 und Ø2,2 sind Durchgangslöcher für M3 und M2, die Allgemeintoleranz ISO 2768-m reicht (±0,1 auf die Durchmesser, ±0,3 bzw. ±0,5 auf die Lagen). Deshalb auch keine Abmaßtabelle.
- 23.11.: Sammelangaben neben dem Schriftfeld: Oberfläche „lasergeschnitten“ (Grundsymbol mit Verfahren, ohne Rz-Wert), Kanten −0,5 nach ISO 13715 (gratfrei bis 0,5 mm, wie in den Musterzeichnungen des Betreuers).
- 23.11.: Halbzeug „Sperrholzplatte 500x470x5“.

## Freiraum (Regel 4)
- Schalenrand 105 mm über Boden (Räder 80 + 20 + 5 Reserve). Freiraum gilt ab 85 mm, Kreis Ø262.
- Ursprünglicher Plan: alles außer Podest und Schale unter 85 mm über Boden (59,5 über Plattenoberseite). Für die Haube seit 17.11. aufgehoben, Finnen reichen bis 94 über Platte.
- Podest oberhalb 85 mm nur Rohr Ø36 und Kopf Ø62, ganz unter der Schale Ø102 verdeckt. Lesart beim Veranstalter bestätigen.

## Schale
- Ø101 bis 102 am Rand, Nabe Ø43,2 mit 6 Laschen, 26 g mit Ball.
- 13.11. gemessen: Laschen-Lochkreis Ø49, Löcher passen für M3. Podest-Kopf: 6 Kernlöcher Ø2,7, 7,5 tief, M3 selbstschneidend.
- Die Laschen sind bündig mit der Nabenunterseite, die Mulde Ø43,6 im Kopf zentriert also nicht. Zentriert wird über die 6 Schrauben.
- Gesamthöhe der Schale nicht gemessen, sie ist deutlich höher als die angenommenen 12,3 mm. Damit liegt der Rand über 105 mm.

## Start und Strom
- Startknopf ist der Wippschalter (Hauptschalter) zwischen Akku und MDD3A. Vom MDD3A 5VO geht ein Kabel zur roten Schiene des Steckbretts.
- Wippschalter oben im Bedienpult links neben dem Podest (Ausschnitt 27,2 × 12,2 bei x 38, y 60).
- Code: nach dem Booten 3 s warten, dann losfahren (Regel: 2 bis 10 s an der Startwand).
- 5VO laut Cytron-Datenblatt max. 200 mA, WLAN aus lassen.
- Beim Veranstalter fragen, ob der Wippschalter als Startknopf zählt. Ersatz: Stoßschalter vorne als Start.

## Startwand (Regeln v1.0, Zeichnung S. 3)
- 50 × 50 cm, beweglich. Die ganze Wand ist der Sensor, jede Berührung irgendwo auf der Fläche löst aus.
- Haubenanschlag: 76 breit, 25 bis 50 mm über Boden, 4 mm hinter allem anderen. Er legt den hintersten Punkt fest und schützt die Finnen beim Anfahren.

## Platte
- Sperrholz 5 mm, 256 × 170 (x −86 bis +170, y ±85), Ecken R8, gerade Hinterkante. Ca. 153 g. Gelasert mit 47 runden Löchern, 1:1 wie das damalige Modell. Im Modell seit 20.11. nur noch 37 Löcher (siehe Entscheidungen).
- Hinten 10 mm freier Streifen (x −86 bis −76) hinter der Steckbrett-Wanne für die Haubenschrauben.
- Motorwinkel wie V1: Löcher x ±10,85, |y| 76,5 und 44,75.
- Podest 4 × M3 auf LK Ø46 um (40, 0). Kugelrolle 2 × M2 bei (150, ±7,75).
- MDD3A 4 × M3 bei x 19,25 / 61,25 und y −34,5 / −71,5. Platine laut Team-Baugruppe x 17 bis 65,5.
- Stoßschalter 2 × M3 × 30 bei (160, ±11,1), Lochabstand 22,2. Unter dem Schalter 2 Muttern als Abstand, weil die Kugelrollen-Schrauben hochstehen. Schalterkörper laut Team-Baugruppe x 136,8 bis 166, y ±15, z 3,6 bis 16,6, Hebel bis x 175. Der Frontsensor-Halter liegt bei z 16,5 darauf, oben 2 Muttern.
- Akkurahmen vorne 2 × M3 × 16 bei (140, ±26), Mutter oben auf der Platte, Schraube bis z 5,5.
- Haube 7 × M3 in den vorhandenen Löchern: H1–H3 (−81 / 60, 0, −60), H4/H5 (130 / ±78), H6/H7 (162 / ±45). Keine neuen Löcher nötig.
- M3 gezeichnet Ø3,2, M2 Ø2,2.

## Antrieb (gemessen 20.11.)
- Räder Ø80, ca. 9,2 breit, innen bei y ±89,7, außen bei ±99,0.
- Getriebe-Stirnseite bei y ±73,8, dazwischen freie Welle bis zum Rad. Achse z 14,5.
- In der Creo-Baugruppe sitzen die Räder zu weit außen (Stand 23.11.: ±95,5 bis ±107,8).

## Anbauteile
- Echo-Halterungen (`cad/stl/halterung-l-echo.stl`, `-r-echo`, `-v-echo`; alle drei derselbe Körper, nur die Löcher verschieden): 52 lang, 17 tief, 26,5 hoch. Fuß 4 dick, Löcher Ø3,4 bei 8,5 von der Rückseite. Zwei Pfosten 8 breit an den Enden, Platinenschlitz 2,7 bis 5,95 hinter der Rückseite, entlang 3,3 bis 49,1 (Mitte 26,2), Schlitzboden 6 über dem Fuß-Boden. Niedrige Rückwand bis 7,5.
  - Rechts (Löcher 5,5 / 39,5 ab Ende): x 66,5 bis 118,5, 2 mm vor dem MDD3A. Kapselmitten x 79,7 und 105,7.
  - Links (Löcher 10 / 44 ab Ende): x 64 bis 116, 2 mm hinter dem Bedienpult. Kapselmitten x 76,8 und 102,8.
  - Vorne (Löcher 14,9 / 37,1, Abstand 22,2): auf dem Stoßschalter x 151,5 bis 168,5, Schlitzmitte bei y +0,2.
  - Kapselspitzen bei y ±72,5 (Platine im Schlitz frei, bis 73,75 möglich, für die Haube unkritisch). Kapselmitte z 16,25 (vorne 16,8 höher).
- HC-SR04: Platine 45,4 × 20,5 × 1,2, Kapseln Ø16 im Abstand 26, Kapselspitze 12,3 mm vor der Platinen-Vorderseite. Auf der Vorderseite zwischen den Kapseln der Quarz 11,3 × 4,9 × 3,4, am anderen Rand Lötstellen der Stiftleiste 1,7 mm hoch. Im Halter mit den Stiften nach oben eingebaut.
- Tasteraufsatz: Bügel 80 breit, 10 hoch (z 6 bis 16), Hülse auf dem Stößel. Stößelspitze ca. x 177,6.
- Akku-Schienen-Rahmen unter der Platte, Akku von hinten eingeschoben, vorne bei x 140, y ±26 verschraubt. Bodenfreiheit nur ca. 2,4 mm.

## Haube V4
- Ersetzt V1 bis V3: Echos sollen wie Waffen aus der Haube schauen, Haube seitlich nicht breiter als die Echos (nur unten bis zur Platte), Heck kein Klotz.
- Rumpf ±68, Dach z 58, unten bis z −3 (3-mm-Rand über die Plattenkante, 0,3 mm Luft). Flanke ±88 bis x 67, Oberkante z 48 (Kabelraum). Keilnase mit offener Bucht y ±28 für Frontsensor und Stoßschalter. Seit 23.11. ist die Nase unten hinten offen (keine Rückwand bei x 140 bis 142 unter z 20), damit Stoßschalter und Akkurahmen-Schrauben frei sind.
- Rohrblende: Doppelrohr wie die schwarze Blende vom Foto, Bohrungen Ø16,4 auf den Kapseln Ø16, 8,4 mm tief, Vorderseite bündig mit den Kapselspitzen. Hinten 0,5 mm Luft über dem Quarz. Dreimal dasselbe Teil, je ca. 5 g.
- An den Seitenechos ein unten offener Einschnitt, weil die Haube von oben über die waagerechten Kapseln gesetzt wird. Reihenfolge: Blenden auf die Kapseln, dann Haube drüber. Fußschlitz seit 23.11. bis z 6,5 (vorher 4,5).
  - Links: Bögen R12,5 um x 76,8/102,8, Enden x 68,3 und 111,3, Fußschlitz x 62,5 bis 117,5.
  - Rechts: Bögen R12,5 um x 79,7/105,7, Enden x 71,2 und 114,2, Fußschlitz x 62,5 bis 120.
- Kotflügel mit rundem Radlauf R46 um die Achse ab y 71 nach außen, hinten 10 mm dünne Finnen bis z 94.
- Radkasten (20.11.): Radlauf R46 bis zur Platte verlängert (unter der Achse senkrecht bei x ±46), ab |y| 71 offen. Keine Wand und kein Wellenschlitz mehr zwischen Rad und Motor. Reifen 6 mm zum Radlauf, Motor und Welle mindestens 19 mm.
- Heck: Mittelteil (y ±40) bei x −89, Seiten bei x −86,3. Anschlag 76 breit, z 0 bis 24, bis x −93.
- Dachloch Ø66 um das Podest, kleiner geht nicht wegen des Podestkopfs Ø62.
- Schalterschacht x 20 bis 60, y 45 bis 67 (bis über die Teilung, sonst bliebe ein 2-mm-Steg).
- Teilung (20.11.) bei x 58, bündig mit der Kotflügel-Vorderkante. Heck: x −93 bis 58 mit ganzem Kotflügel, Radkasten, Schalterschacht und H1–H3. Front: x 58 bis 170 mit Echo-Einschnitten, Nase und H4–H7. Beide Teile nur bei abgenommener Schale ab- und aufsetzen.
- Kabelraum: über MDD3A mindestens 27 mm frei, über den Motoren mindestens 19 mm, über dem Steckbrett mindestens 15 mm. Die Flanken-Stirnwand steht 0,5 mm vor dem MDD3A, Kabel dort nicht nach vorne herausführen.
- Befestigung: 7 × M3 × 16 von unten durch die Platte, Scheibe unter dem Kopf.
  - H1, H2, H3 (Heckteil): Pfeiler mit Durchgangsloch Ø3,4 und seitlicher Mutterntasche (5,7 breit, 2,7 hoch, ab z 6, nach vorne offen). Mutter vor dem Aufsetzen einlegen, flache Seite an die Taschenwand (Klebeband), danach hält die Steckbrett-Wanne 1 mm davor sie fest.
  - H4, H5: Schraubfuß außen am Rumpf (x 124 bis 136, y 66 bis 84, 6 dick). Oben Scheibe und Mutter.
  - H6, H7: Fuß unter der Nase (x 149 bis 168, y 39 bis 51, 6 dick) an einer Stütze zum Nasendach. Oben Scheibe und Mutter, seitlich unter der Nase erreichbar.
  - Löcher nach dem Druck mit 3,5 mm aufbohren.
  - Zum Code-Ändern Schale ab, H1–H3 lösen und das Heck abheben.
  - Einkauf: 7 Schrauben M3 × 16 (ISO 4762 oder 7380), 7 Muttern M3 (ISO 4032), 11 Scheiben M3 (ISO 7089).
- Geprüft gegen alle Bauteile, Halterungen exakt nach den STLs: keine Überschneidung. Engste Stellen: Kapsel zu Rohrblende 0,2 mm (Klemmsitz), Rohrblende zu Haube 0,5 mm, Halterungen zur Haube 0,5 mm (vorne 2 mm), Schallkegel mindestens 0,57 mm (±15° ab Kapselspitze), Quarz zu Rohrblende 0,5 mm, MDD3A 0,5 mm, Steckbrett-Wanne 1,0 mm, Bedienpult 1,1 mm, Plattenkante 0,3 mm, Reifen 6 mm (Räder nach Messung 20.11.).
- 23.11. zusätzlich gegen alle Teile der Team-Baugruppe `batmobile-v2` geprüft (außer deren Rädern, dafür die gemessenen): keine Überschneidung. Engste Stellen: Klemmen vom MDD3A 0,14 mm zur Flankenwand (Platine in der Baugruppe 1 mm weiter vorne als angenommen), Seitensensor 0,3 mm, Rohrblenden und Halter 0,5 mm, Schrauben der Echo-Halter 1,4 mm. Die Muttern von H1–H3 sind in der Baugruppe über Eck gedreht und ragen aus der Tasche, richtig eingelegt passen sie.
- Beide Teile lassen sich senkrecht von oben aufsetzen, nur die Schale muss vorher ab.
- Zwei Druckteile (Stand 23.11.): Heck 141,8 cm³ (176 g PLA), Front 56,1 cm³ (70 g), Rohrblende 3,96 cm³ (4,9 g).
- Druck auf dem Bambu Lab X1E (Bett 256 × 256): flach passen Front und Heck nicht zusammen aufs Bett (263 mm). Deshalb in einem Auftrag beide auf der Schnittfläche x 58 stehend (Heck 151 hoch, Front 112 hoch, die STL-Dateien liegen schon so), PLA Basic für Teile und Stützen, 0,20 mm, 15 % Füllung, Baumstützen nur auf Druckplatte, Brim 8 mm nur für Front und Heck. Löcher H4–H7 liegen dabei waagerecht, nach dem Druck aufbohren.
- STEP-Baugruppe `cad/haube_v4/Haube_V4.stp` (AP214, mm): HAUBE_V4 mit HAUBE_HECK, HAUBE_FRONT und dreimal ROHRBLENDE. Koordinaten wie die Baugruppe (Creo X = x, Creo Y = z, Creo Z = −y), in `roboter_v2` mit Default platzieren. Jedes Teil ein geschlossener Volumenkörper, kürzeste Kante 0,78 mm.
- Gegenüber der Creo-Anleitung geändert: Fase Schritt 5 ab y 77 statt 76, hintere Seitenteile Schritt 7 bei x −86,3 statt −86, Kotflügelspitze Schritt 8 bei x −80 statt −82, Radlauf Schritt 9 ab y 71 statt 70, Knick der Verjüngung Schritt 10 bei x 12 statt 16, Schnitt Schritt 13 an Seiten und hinten 0,3 größer, Schalterschacht Schritt 15 x 20 bis 60 und bis y 67, Wellenschlitz Schritt 17 ersetzt durch offenen Radkasten, Einschnitt links Schritt 18a neu, Fußschlitz der Einschnitte bis z 6,5, untere Rückwand der Nase entfernt, Teilung Schritt 26 bei x 58 statt −15.

## Haube V1 (17.11., überholt)
- Kantiger Panzer-Look mit Schulterkästen, Turmöffnung Ø110, Heckschild 176 breit, 7 × M3 × 16 selbstschneidend in Kernloch Ø2,7. Vom Team abgelehnt, ersetzt durch V4.

## Anordnung
- Hinten quer: Steckbrett + ESP32 in Druckwanne (x −76 bis −21,1). Mitte: Motoren, Podest (x 40), links Bedienpult mit Wippschalter, rechts MDD3A.
- Vorne: Kugelrolle, Sensor-Aufsatz auf dem Stoßschalter, Tasteraufsatz. Akku darunter im Schienen-Rahmen.
- Räder innen bei y ±89,7 (gemessen 20.11.).

## Rechenwerte
- Masse ca. 850 g ohne Haube, Schwerpunkt x 41, y 0, 37 mm über Boden (Stand vor dem Umzug des Akkus nach unten). Mit Haube V4 und Blenden ca. 1110 g.
- Ball: Startwert a_max 0,3 m/s², Rampe 0,3 s, Kriechen 0,05 m/s an der Endwand, Pause 1 s. Nach Kipptest ggf. bis 0,8.
- Akkupack 17,5 mm hoch (gemessen 13.11.).

## Offen
- Front (Stand 23.11.) neu drucken und am Roboter prüfen. Heck und Rohrblenden vom 20.11. bleiben.
- Räder in der Creo-Baugruppe auf die Messung setzen (innen ±89,7), dann `Haube_V4.stp` einbauen, PLA zuweisen.
- Schalenrand über Boden messen: Dupont-Stecker am Frontsensor reichen bis ca. 85 mm, Rand muss mindestens 106 mm hoch sein.
- Motorlänge mit Encoder.
- Beim Veranstalter: Podest-Lesart, Wippschalter als Start.
- Podest-Loch im Modell korrigieren: eins sitzt bei (56,0 / −16,26) statt (56,26 / −16,26) auf dem Lochkreis Ø46. In der Zeichnung steht deshalb 142 statt 142,26.
- Klären, welcher Stand gilt: gelaserte Platte und DXF mit 47 Löchern oder Modell und Zeichnung mit 37.
- Zeichnung fertig machen: Ordinate x 236 (Kugelrolle) fehlt, Maß 5 an der Isometrie löschen (Dicke steht schon als t=5), „-0.5“ als „-0,5“ schreiben. Optional das Maß 8 durch die Ordinate 248 ersetzen.
