# Flussdiagramm `code/wallsprint.py`

Werte wie im Code: VMAX 70 %, Kriechen 15 %, Bremsen ab 40 cm (Echo), Kriechen ab 15 cm, Rueckfahrt bremst ab 40 cm Rest, Takt 50 ms.
In jeder Schleife gilt: nach 60 s Motoren aus und Abbruch.

```mermaid
flowchart TD
    A(["Start"]) --> B["Motoren aus"]
    B --> C{"Taster schon gedrueckt?"}
    C -- ja --> C1["FEHLER ausgeben, nicht losfahren"] --> Z1(["Ende"])
    C -- nein --> D["Echo 3x messen und ausgeben"]
    D --> E["3 s warten"]
    E --> F["Startzeit merken, Encoder auf 0, Tempo = 0"]

    F --> H1["Abstand messen (Median aus 3)"]
    H1 --> H2{"Abstand > 40 cm und Taster nicht gedrueckt?"}
    H2 -- ja --> H3["Tempo + 5 %, hoechstens 70 %"]
    H3 --> H4["vorwaerts fahren, 50 ms warten"]
    H4 --> H1

    H2 -- nein --> B1{"Taster gedrueckt?"}
    B1 -- nein --> B2{"Abstand > 15 cm?"}
    B2 -- ja --> B3["Soll-Tempo aus Abstand: 70 % bei 40 cm bis 15 % bei 15 cm"]
    B2 -- nein --> B4["Soll-Tempo = 15 % (Kriechen)"]
    B3 --> B5["Tempo hoechstens 6 % pro Takt runter"]
    B4 --> B5
    B5 --> B6["vorwaerts fahren, 50 ms warten, Abstand messen"]
    B6 --> B1

    B1 -- ja --> W1["Motoren aus"]
    W1 --> W2["Ausgabe Wand, FEHLER wenn nicht gebremst oder zu schnell"]
    W2 --> W3["Zeit, Strecke und Impulse L und R merken"]
    W3 --> W4{"Strecke > 20 cm? (Encoder zaehlen)"}
    W4 -- ja --> W5["Rueckfahrt nach Impulsen"]
    W4 -- nein --> W6["Rueckfahrt nach Zeit"]
    W5 --> W7["700 ms an der Wand warten, Encoder auf 0"]
    W6 --> W7

    W7 --> R1{"Ziel erreicht? (Impulse oder Zeit)"}
    R1 -- nein --> R2["Soll-Tempo: 70 %, ab 40 cm Rest runter bis 15 %"]
    R2 --> R3["Tempo sanft anpassen: erst kleine, dann groessere Schritte hoch, hoechstens 8 % runter"]
    R3 --> R4["Rad, das fertig ist, anhalten"]
    R4 --> R5["rueckwaerts fahren, 50 ms warten"]
    R5 --> R1

    R1 -- ja --> S1["Motoren aus, Impulse ausgeben"]
    S1 --> S2{"Encoder zaehlen?"}
    S2 -- ja --> S3["mit 15 % rueckwaerts, bis die Raeder 200 ms stehen oder 15 cm extra"]
    S2 -- nein --> S4["1,5 s mit 15 % rueckwaerts"]
    S3 --> S5["Motoren aus, Fahrzeit ausgeben"]
    S4 --> S5
    S5 --> Z2(["Ende"])
```

`code/wallsprint_drehung.py` hat zusaetzlich in der Hinfahrt: nach 100 cm bis 0 % abbremsen, 0,3 s warten, einmal 360 Grad auf der Stelle drehen (Impulse werden nicht zur Strecke gezaehlt), 0,3 s warten, weiter wie oben.
