# Datenblätter

Auszüge aus den Herstellerunterlagen der Bauteile aus dem Starter Kit. Die Bilder wurden auch im Pitch am 16.10. gezeigt (`doku/praesentationen/2026-10-16_pitch.pdf`). Für Details immer das vollständige Datenblatt über den Link öffnen.

| Datei | Bauteil | Was drinsteht | Quelle |
| --- | --- | --- | --- |
| `esp32-pico-kit-1_board.jpg` | ESP32-PICO-KIT-1 | Aufbau des Boards: Chip, Spannungsregler, USB-UART-Brücke, EN- und Boot-Taster | [Espressif User Guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-pico-kit-1/user_guide.html) |
| `esp32-pico_wlan-strom_tabelle19.jpg` | ESP32-PICO | Strom beim WLAN-Senden bis 370 mA (Kap. 5.4, Tabelle 19) | [ESP32-PICO Datenblatt](https://documentation.espressif.com/esp32-pico_series_datasheet_en.pdf) |
| `fit0520_motor_daten.jpg` | DFRobot FIT0520 | 6 V, Getriebe 1:20, 300 U/min ohne Last, 245 U/min bei bestem Wirkungsgrad, Blockierstrom 2,7 A, Encoder 224,4 Impulse pro Radumdrehung (11 × 20,4), 96 g | [DFRobot Wiki](https://wiki.dfrobot.com/FIT0520) |
| `mdd3a_platine.jpg` | Cytron MDD3A | Anschlüsse: Stromeingang, Motorausgänge, Signaleingänge mit 5-V-Ausgang, Testtaster, Status-LEDs | [Cytron Datenblatt](https://cdn.shopify.com/s/files/1/0176/3274/files/MDD3A_Datasheet.pdf) |
| `hc-sr04_eckdaten.jpg` | HC-SR04 | 2 bis 400 cm, Genauigkeit 0,3 cm, Messwinkel 15°, 5 V, 15 mA | [HC-SR04 Datenblatt (ElecFreaks)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) |
| `hc-sr04_spezifikation.jpg` | HC-SR04 | Spezifikation: 40 kHz, Trigger-Puls über 10 µs, Echo-Puls entspricht dem Abstand | wie oben |
| `eneloop_bk-3mcde_daten.jpg` | Panasonic Eneloop BK-3MCDE | AA, NiMH, 1,2 V, mindestens 2000 mAh, 28 g, Innenwiderstand ca. 25 mΩ (gemessen nach Entladung auf 1,0 V) | [Datenblatt bei RS](https://docs.rs-online.com/bfdc/A700000015963728.pdf) |

## Was wir daraus für den Roboter mitnehmen

- ESP32-Pins vertragen höchstens 3,6 V. Das Echo vom HC-SR04 hat 5 V und geht deshalb über einen Spannungsteiler (`elektronik/pinbelegung.md`).
- GPIO 34 bis 39 können nur lesen und haben keinen internen Pull-up.
- Der 5-V-Ausgang des MDD3A liefert höchstens 200 mA. Beim WLAN-Senden braucht der ESP32 bis zu 370 mA, deshalb bleibt WLAN aus.
- Sind beide Eingänge eines Motors am MDD3A gleich (beide low oder beide high), bremst der Motor. Freies Ausrollen gibt es nicht.
- Vier Akkus liefern zusammen ca. 4,8 V, leer ca. 4,0 V. Das ist genau die Untergrenze des MDD3A, also immer mit vollen Akkus fahren.
- Zwischen zwei Ultraschall-Messungen mindestens 60 ms warten. Abstand in cm = Echo-Pulsdauer in µs ÷ 58.
- Encoder: Das Datenblatt nennt 224,4 Impulse pro Radumdrehung, im Code rechnen wir mit 224 (SBC Kap. 4b, siehe `code/einstellwerte.md`).
