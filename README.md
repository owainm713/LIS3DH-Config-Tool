# LIS3DH-Config-Tool
Python GUI configuration tool for the LIS3DH accelerometer

Simple GUI written in Python to help program LIS3DH accelerometers.
Idea behind this is use it to help program microcontrollers with constrained
memories such as the Arduino or ESP8266 with the bare minimum of amount code 
to get the LIS3DH functioning. This will provide the raw configuration register
values required to write into the LIS3DHs configuration registers to do whatever function
you want

This is not a how-to tool. To figure out the LIS3DH both the datasheet and
app note are extremely valuable.

December 18, 2019 Update
- added microcontroller examples using Arduino, Circuit Python, Lua/NodeMCU (ESP8266)
- these examples use the i2c interface, I might do some SPI examples in the future

January 8, 2019 Update
- added save/open feature, including autosave
- added some templates, may add more as I play around with it more
- added Notes and note editor
