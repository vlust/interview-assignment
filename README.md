# Interview Task

The hardest part of this project was making design decisions. With little to no design, monetary, or other constraints, I decided to base my choices on how interesting I found the solutions—particularly when there was no clear direction provided in the task.

## Task 1

The 4–20 mA interface was not specified, so I assumed a sensor with an integrated transmitter and chose a 100 Ω shunt resistor, expecting a 0.4 V to 2 V voltage output (for different voltage ranges, the shunt resistor would need to be adjusted). If the sensor were just a passive component, a transmitter circuit would be required.

I attempted to build the circuit using components I had available to make the process more engaging. The result is this schematic: [CurrentSensorUSB\_prototype.pdf](hardware/CurrentSensorUSB_prototype/CurrentSensorUSB_prototype.pdf). I didn’t have any components to achieve galvanic isolation between the MCU and the current measurement, but I was able to use the circuit to test the Python data acquisition software. I wrote the firmware in Rust because I had never tried embedded Rust before.

The prototype circuit didn’t fully meet the requirements outlined in the task, so I created another schematic: [CurrentSensorUSB.pdf](hardware/CurrentSensorUSB/CurrentSensorUSB.pdf), along with a BOM: [CurrentSensorUSB.csv](hardware/CurrentSensorUSB/CurrentSensorUSB.csv). A more detailed explanation of the component choices can be found here: [README.md](hardware/CurrentSensorUSB_prototype/README.md).

## Task 2

The `software` folder contains a Python project with a CLI tool that can acquire a data stream over serial and generate a report based on the acquired data. An example report generated using the prototype board can be found here: [report.pdf](software/data/report_20250518_223138.pdf). More information on this task can be found in the README in the software directory: [README.md](software/README.md).


