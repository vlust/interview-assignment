# Interview task
The hardest part of this project was making design decisions. With no or very little design, monetary, or other constraints, I decided to just make decisions based on how interesting I found the solutions (that is, if there was no way of deciding based on the information in the task).

## Task 1

The 4-20mA interface was not specified, so I assumed a sensor with an integrated transmitter and chose a 100 Ohm shunt resistor, expecting a 0.4 to 2V voltage output (for a different voltage output, the shunt resistor would need to be adjusted). If the sensor is just a passive component, a transmitter circuit would need to be added.

I attempted to build the circuit using components I had available to make it more engaging. The result is this schematic: [CurrentSensorUSB_prototype.pdf](hardware/CurrentSensorUSB_prototype/CurrentSensorUSB_prototype.pdf). I didn't have any components to achieve galvanic isolation between the MCU and the current measurement, but I was able to use the circuit to test the Python data acquisition software. I wrote the firmware in Rust because I had never tried embedded Rust before.

The prototype circuit didn't meet the requirements outlined in the task, so I created another schematic: [CurrentSensorUSB.pdf](hardware/CurrentSensorUSB/CurrentSensorUSB.pdf), along with a BOM: [CurrentSensorUSB.csv](hardware\CurrentSensorUSB\CurrentSensorUSB.csv). A more detailed explanation of why I chose those components can be found here: [README.md](hardware/CurrentSensorUSB_prototype/README.md).

## Task 2

The software folder contains a python project with a cli tool which is able to acquire a stream of data over serial and creating a report based on the acquired data. More information on this task is in the readme in the software directory: [README.md](software\README.md)

## Task 3


