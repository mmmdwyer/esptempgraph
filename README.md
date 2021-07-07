= ESP Temp Graph =

Created as an excuse to get a NodeMCU to DO something, it ended up being
a doorway into Micropython. This is intended to run on an ESP8266 "Amica"
NodeMCU device, that's available for cheap from the usual scum.

The documentation for this board is spotty and fragmented, but I found
great value from this site:
https://www.hackster.io/javagoza/nodemcu-amica-v2-road-test-2e8bff
Notably, there's no I2C hardware, and the pin labels on the board don't
match the GPIO# used in code.

To this board, I used esptooy.py to erase the flash, then the same tool to
flash micropython 1.16 to it. I needed to add the -fm dio flag, and I had to
run esptool on my other machine since the version in Ubuntu didn't work 
correctly.  

http://micropython.org/download/esp8266/

Once here, the ampy tool could be used to push files to the board. I had a
loop like this:

vi tempscreen.py ; ampy put tempscreen.py ; ampy run tempscreen.py

I parked the board in a breadboard. I am currently powering it though its
USB plug. Then, I used the 3v3 and GND pins coming from the onboard voltage 
regulator to power the sensor and display.

The sensor is a DHT11, which can also be found from the usual scum for really
cheap.  The board I bought came pre-mounted on a small board, that included 
the recommended pullup resistor and a capacitor on the rails. It also dropped
the useless NC pin, and instead drops to a 3-pin right-angle header that is 
easy to push into a breadboard. It has a nasty protocol and terrible precision. But it's cheap.

The sensor was wired to D1 on the board, which is GPIO5.

The display is an ssd1306-based OLED 128x64 display that are also available
from the usual scum for almost no money.  This one, again, was pre-mounted to
a breadboard-friendly carrier, exposing the four pins.

The display was wired from SCL to D2 (GPIO4) and SDA to D3 (GPIO0).

I originally struggled to get I2C working until I read that site closer to 
see that, despite pins labeled CLK and SD0, that you must use SoftI2C!

Micropython makes running this display and sensor SUPER easy, with built-in
support libraries for them.  I just needed to import dht and ssd1306. 

The code reads the whole-number centigrade temp and whole-percentage humidity,
then stores that in a looping 128-slot array -- the same width as the display.

I mod%64 the number, and this naive approach actually works really well for 
room temperatures in C and reasonable humidities. I paint a vertical bar
to show where the current time pointer is. Then I paint the current numeric
temp and humidity near the bar, near their line.

I put a fair amount of logic into this logic; it will try not to fall off the
screen, and will try not to overwrite the other text.

There's no scale, and no scaling.  It think it looks interesting, but it is
meant to give you an overview of the local weather's ups and downs, while 
not caring about the actual numbers all that much.

Lastly, I include the boot.py file, because I had to change it to turn off
esp debug, as Micropython recommended.  I should also turn off the ESP radio
in there -- or give it my real wifi -- and I will eventally want to make
it boot my code at power-up, instead of having to run it from the serial REPL
or ampy every time.

More FIXMEs are in the files.

