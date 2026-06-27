# hello_world.py

from machine import Pin, SPI
from ili9341 import ILI9341, color565

backlight = Pin(21, Pin.OUT)
backlight.value(1)

spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

dummy_rst = Pin(4, Pin.OUT)
dummy_rst.value(1)

display = ILI9341(spi, cs=Pin(15), dc=Pin(2), rst=dummy_rst, w=320, h=240, r=0)

display.set_color(color565(0, 0, 0), color565(255, 255, 255))
display.erase()
display.reset_scroll()

display.set_pos(2, 5)
display.print("Hello World!")

print("Done - check the screen")
