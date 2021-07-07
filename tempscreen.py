from machine import Pin, SoftI2C
import dht
import ssd1306
import time
import uarray

# Setup Here

# FIXME shut down the wifi chip

d = dht.DHT11(machine.Pin(5))  # NodeMCU D1
i2c = SoftI2C(scl=Pin(4), sda=Pin(0), freq=100000) # D2, D3
display = ssd1306.SSD1306_I2C(128, 64, i2c)
# Puts an straight diagonal line in data
temphist=uarray.array('b',range(0,128))
humihist=uarray.array('b',range(0,128))
histpointer=0

while True:
    d.measure()
    temp = d.temperature()
    humi = d.humidity()
    temphist[histpointer]=d.temperature()
    humihist[histpointer]=d.humidity()

    display.fill(0)

    # Vertical line showing where NOW is.
    display.line(histpointer,0,histpointer,64,1)

    # Display the degrees number near the current temp
    humix=histpointer
    tempx=histpointer
    humiy=64-(humi%64)
    tempy=64-(temp%64)

    # Normally go 3px to the right
    if (histpointer<100) :
        humix += 3
        tempx += 3
    else : # Unless too close to the edge, then go left
        humix -= 28
        tempx -= 28

    # If temp and humidity would overdraw, split them
    while abs(tempy-humiy) < 5 :
        if (tempy < humiy) :
            tempy -= 1
            humiy += 1
        else :
            tempy += 1
            humiy -= 1

    # If I'm near the bottom, don't go any further - FIXME
    if humiy > 60 :
        humiy = 60

    if tempy > 60 :
        tempy = 60

    # Finally draw the text
    display.text("{}C".format(temp), tempx, tempy, 1)
    display.text("{}%".format(humi), humix, humiy, 1)

    # Debug aid
    # display.text(str(histpointer), 64, 20, 1)

    # Paint the graph lines
    # FIXME: I'm just fortunate that my mod64 wrapper puts 
    # lines is a good vertical position. But how could I do
    # this better? Take averages, and locate those as middle 
    # +20 and middle -20?
    for X in range(128) :
        display.pixel(X,(64-temphist[X]%64),1)
        display.pixel(X,(64-humihist[X]%64),1)

    display.show()
    
    time.sleep(500)

    # Increment history pointer
    histpointer = histpointer + 1
    if (histpointer > 127) :
        # FIXME: When screen is filled, store to FLASH so it is
        # prettier on restart?
        histpointer=0



