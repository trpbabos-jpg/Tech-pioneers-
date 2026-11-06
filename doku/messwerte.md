# Messwerte

Neue Messungen unten mit Datum anhängen. Für die Bewertung brauchen wir am Ende die Durchschnittsgeschwindigkeit auf 200 cm.

## 23.10.2026: Drehzahl ohne Räder

- Methode: ESP32 zählt 1 s lang die Encoder-Impulse, 224 Impulse pro Radumdrehung
- Formel: U/min = Impulse ÷ 224 ÷ Zeit (s) × 60
- Bei 100 %: Motor 1 = 244 U/min, Motor 2 = 247 U/min
- Motor 2 dreht gut 1 % schneller, deshalb Ausgleichsfaktor beim Geradeausfahren

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
