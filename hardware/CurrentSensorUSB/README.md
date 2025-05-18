# Design Considerations

## 1. Microcontroller (U1: ATSAMD21E18A‑A)

* **Why chosen**:

  * **Built‑in USB Full‑Speed interface** simplifies serial‑over‑USB implementation.
  * Proven ecosystem and popularity
  * E‑Series package (smallest) has more than enough GPIO and ADC channels for this project.

---

## 2. Precision ADC (U3: ADS1113IDGS)

* **Why chosen**:

  * **16‑bit resolution** yields better than 10 µA resolution over the 4–20 mA span by adjusting the PGA settings.
  * Single‑ended input with onboard reference minimizes external parts.
  * I²C interface maps cleanly to the SAMD21 peripheral.

---

## 3. Digital Isolator (U5: ADuM1250)

* **Why chosen**:

  * Provides **2.5 kV galvanic isolation** on I2C lines.
  * Ensures USB‑side ground is fully isolated from the analog front end.

---

## 4. DC–DC Converter (PS1: MEE1S0503SC)

* **Why chosen**:

  * Generates an **isolated 3.3 V rail** from USB 5 V for the sensor‑side analog domain.
  * 150 mW output rating covers the ADS1113 + op‑amps + isolator.

---

## 5. Shunt Resistor (R2: 100 Ω LVK12)

* **Why chosen**:

  * Converts 4–20 mA into 0.4–2.0 V (with gain stage, maps to 0.2–1.0 V for the ADS1113).
  * **0.1 % tolerance** keeps measurement error < ±1 µA.

---

## 6. Voltage Regulator (U2: MCP1703A‑3302)

* **Why chosen**:

  * **3.3 V LDO** for the SAMD21 from the USB 5 V rail.

---

## 7. ESD Protection (D1: PRTR5V0U2X)

* **Why chosen**:

  * I wanted to incoorperate an example for circuit protection but without having a clear safety bufget i decided to keep it minimal.

---

## 8. 32.768 kHz Crystal (Y1)

* **Why chosen**:

  * Provides a **precision RTC clock** for timestamping the serial out.
  * Matched load capacitance (6.8 pF) aligns with the SAMD21’s XOSC32K requirements.