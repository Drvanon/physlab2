# physlab2
A project used as a driver and data analysis tool for the course Physics Laboratory 2 at the Rijks Universiteit Groningen.

## Stepper motor driver
The arduino driver available in `arduino/main`is to be used as a simple driver for a stepper motor that is driven by the DRV8825 chip. The code is easily compatible with other chips, such as the DRV8830 or the A4988 driver. It provides an interface so that the serial communication port can be used to start and stop measurements, set stepsize or reverse.

## Scale
For this project it was neccessary to use a scale as a way to measure forces. We have used the HX711 chip to read out a 5kg load cell. The aforementioned serial communication can also be used to tare the devices. 
