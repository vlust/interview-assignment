# Interview Task

The hardest part of this project was making design decisions. With little to no design, monetary, or other constraints, I decided to base my choices on how interesting I found the solutions—particularly when there was no clear direction provided in the task.

## Task 1

The 4–20 mA interface was not specified, so I assumed a sensor with an integrated transmitter and chose a 100 Ω shunt resistor, expecting a 0.4 V to 2 V voltage output (for different current ranges, the shunt resistor would need to be adjusted). If the sensor were just a passive component, a transmitter circuit would be required.

I attempted to build the circuit using components I had available to make the process more interesting. The result is this schematic: [CurrentSensorUSB\_prototype.pdf](hardware/CurrentSensorUSB_prototype/CurrentSensorUSB_prototype.pdf). I didn’t have any components to achieve galvanic isolation between the MCU and the current measurement, but I was able to use the circuit to test the Python data acquisition software. I wrote the firmware in Rust because I had never tried embedded Rust before.

The prototype circuit didn’t fully meet the requirements outlined in the task, so I created another schematic: [CurrentSensorUSB.pdf](hardware/CurrentSensorUSB/CurrentSensorUSB.pdf), along with a BOM: [CurrentSensorUSB.csv](hardware/CurrentSensorUSB/CurrentSensorUSB.csv). A more detailed explanation of the component choices can be found here: [README.md](hardware/CurrentSensorUSB/README.md). I couldn’t write the firmware for this circuit because I didn’t have the hardware or toolchain to test it.

## Task 2

The `software` folder contains a Python project with a CLI tool that can acquire a data stream over serial and generate a report based on the acquired data. An example report generated using the prototype board can be found here: [report.pdf](software/data/report_20250518_223138.pdf). More information on this task can be found in the README in the software directory: [README.md](software/README.md).

## Task 3

### 1. Procurement and Documentation

* **Bill of Materials (BOM):**

  * List each component’s reference designator, manufacturer part number, quantity, package, and tolerance. ([BOM](hardware/CurrentSensorUSB/CurrentSensorUSB.csv))

* **Supplier Selection:**

  * Order from authorized distributors (e.g., Digi‑Key, Mouser).
  * Verify lead times (aim for < 8 weeks) and minimum reel‑quantities match production volume.

* **Files for Suppliers:**

  * **PCB Fabricator:** Gerber RS‑274X package (copper, mask, silkscreen, drill), board outline (DXF/PDF), impedance spec (90 Ω differential for USB lanes).
  * **Assembly House:** BOM, pick‑and‑place (centroid) file, paste‑mask Gerbers, assembly drawing PDFs.

---

### 2. Manufacturing Steps

1. **PCB Fabrication (DFM Review)**

   * Ensure trace/space, via sizes, and 2.5 mm isolation clearance meet standards.
   * Four‑layer stack‑up (2 signal, 2 power/ground) for stable analog and controlled‑impedance USB. (Optional: separate isolation layers, though I didn’t have time to finish that layout, and it wasn’t required in the task description.)

2. **Assembly (PCBA)**

   * Provide a laser‑cut stencil for solder paste.
   * Match the reflow profile to the most temperature‑sensitive IC.
   * Perform post‑reflow AOI to catch solder defects. Since no QFN parts are used, X‑ray inspection is not necessary.

3. **Firmware Provisioning**

   * Use a simple SWD/JTAG fixture and ST‑Link (or equivalent) to program each MCU with the final Rust firmware binary.
   * It may be advisable to build a small dev board with a USB bootloader and debugger for a better firmware development experience (the current design has only SWD headers).

---

### 3. Testing and Calibration

* **Incoming Inspection (IQC):**

  * Sample critical parts (shunt resistor, op‑amp, isolator) to verify values and functionality.

* **In‑Process Checks:**

  * **Bare‑Board Test:** Use flying‑probe or ICT to catch opens/shorts.
  * **Power‑Up Smoke Test:** Limit current to \~100 mA, verify no excessive draw or heating.

* **End‑of‑Line Functional Test (FCT):**

  1. **USB Enumeration:** Ensure the board appears as a CDC/Serial device; verify VID/PID and basic loopback.

  2. **Current‑Loop Accuracy:**

     * Use a 4–20 mA precision source (≤ 0.01 % accuracy) to apply five setpoints (4, 8, 12, 16, 20 mA).
     * Read back ADC counts via USB; compute offset and gain error.
     * Adapt the Python data acquisition tool to create automatic reports (see [report\_20250518\_223138.pdf](software/data/report_20250518_223138.pdf)).
     * The MCU should communicate the firmware version and serial number on startup to build that identifier into the report.

  3. **Calibration:**

     * Adjust offset (at 4 mA) and gain (at 20 mA) by programming compensation coefficients into flash. (Trim resistors could also be added to the board for calibration.)
     * Verify mid‑point (e.g., 12 mA) to confirm linearity within tolerance.

  4. **Isolation Test:**

     * Perform a hipot test between the USB side and the sensor side to confirm isolation and leakage requirements.

* **Traceability:**

  * Assign each board a serial number; record calibration data (offset/gain) and test results in a simple CSV or database, with links to the generated reports.

---

### 4. Required Equipment & Files Summary

| **Category**             | **Files/Supplies**                                           | **Equipment**                                                                                              |
| ------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **PCB Fab**              | Gerbers, drill file, board outline (DXF/PDF), impedance spec | —                                                                                                          |
| **PCB Assembly**         | BOM (incl. alternates), pick‑and‑place, paste‑mask Gerbers   | Pick‑and‑place machine, reflow oven, AOI                                                                   |
| **Firmware/Programming** | Final Rust `.bin`/`.hex`, programming script, README         | SWD/JTAG programmer (ST‑Link), PC                                                                          |
| **Functional Testing**   | Test‑fixture drawing, FCT script (Python), calibration doc   | 4–20 mA precision source (e.g., Keithley), 6½‑digit DMM, oscilloscope, USB protocol analyzer, hipot tester |
