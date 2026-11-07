# Messwerte

Neue Messungen unten mit Datum anhängen. Für die Bewertung brauchen wir am Ende die Durchschnittsgeschwindigkeit auf 200 cm.

## 23.10.2026: Drehzahl ohne Räder

- Methode: ESP32 zählt 1 s lang die Encoder-Impulse, 224 Impulse pro Radumdrehung
- Formel: U/min = Impulse ÷ 224 ÷ Zeit (s) × 60
- Bei 100 %: Motor 1 = 244 U/min, Motor 2 = 247 U/min
- Motor 2 dreht gut 1 % schneller, deshalb Ausgleichsfaktor beim Geradeausfahren

## 29.10.2026: Kalibrierung in der Luft (nach dem Umstecken von Motor 1)

- kalibrieren.py, erste Messung: links dreht ab 20 %, rechts ab 16 %
- drehzahl_test.py, Räder frei, Unterschied links zu rechts:

| Stufe | Anlauf 20/16, ohne Faktor | Anlauf 20/20, Faktor 0,94 |
| --- | --- | --- |
| 15 % | +18,7 % | +0,4 % |
| 25 % | +14,2 % | −0,3 % |
| 50 % | +8,2 % | −1,0 % |
| 75 % | +5,6 % | −1,3 % |
| 100 % | +4,4 % | −4,4 % |

- Mit Anlauf 20/20 und Faktor 0,94 bei 100 %: links 230 U/min, rechts 241 U/min
- Kontrolle mit kalibrieren.py: beide Räder drehen ab 20 %

## 29.10.2026: Fahrt auf dem Boden

| Messung | Wert |
| --- | --- |
| Vmax bei 100 % | ca. 84,5 cm/s |
| Geschwindigkeit bei 50 % | ca. 50 cm/s |
| Kriechen bei 15 % | ca. 21 cm/s |
| Bremsbeginn | ca. 60 cm vor der Wand |
| Stopp | 13,1 cm vor der Wand (Ziel 15 cm) |
| Ausrollen | ca. 1 bis 2 cm |

## Noch offen

- Geradeausfahrt: seitliche Abweichung auf 200 cm (3 Mal messen)
- Durchschnittsgeschwindigkeit auf 200 cm (3 Mal messen)
- Bremsen mit Ball in der Schale
