# ESP32 + ILI9341 Display — Learning Notes

Personal storage for ESP32 MicroPython scripts, notes, and things learned along the way.

## Hardware

- **Board:** Hosyond 2.8" ESP32 Display (ESP32-32E module), resistive touch, ILI9341 driver, 240x320 TFT

### LCD pin mapping (specific to this board)
| Function | GPIO |
|---|---|
| CS | IO15 |
| DC | IO2 |
| SCK | IO14 |
| MOSI | IO13 |
| MISO | IO12 |
| RST | shares EN pin (no separate GPIO) |
| Backlight | IO21 (high = on) |

## Software setup

**1. Flash MicroPython firmware**

Installed `esptool`:
```
pip install esptool
```

Erased flash and wrote firmware (generic ESP32 build, not S2/S3/C3):
```
esptool --port COM5 erase-flash
esptool --port COM5 --baud 460800 write-flash -z 0x1000 firmware.bin
```

Confirmed working on `MicroPython v1.28.0`, Generic ESP32 module.

**2. VSCode + Pymakr**

Installed the Pymakr extension in VSCode to upload/run `.py` files directly on the board over serial (COM5, CH340 USB-serial chip — driver was already installed in Windows).

`main.py` auto-runs on every power-up; all other files are imported manually or used as modules.

## Display driver

Started with `rdagger/micropython-ili9341` (`ili9341.py`). This worked fine for single text draws, but its `draw_text8x8()` function reliably corrupted into solid gray blocks whenever more than one draw call happened in the same script (confirmed through extensive isolated testing — not a wiring, SPI speed, or timing issue). Root cause was never fully pinned down at the code level, so the driver was swapped out instead of patched.

**Switched to `jeffmer/micropython-ili9341`** (`ili934xnew.py`, renamed `ili934.py`), which requires a companion font file `glcdfont.py`. This driver's built-in `.print()` method handles word-wrap and auto-scrolling, so no manual text-wrapping helper functions are needed.

### Known quirks of this driver

- `w`/`h` arguments get internally swapped depending on `rotation`. For this board's portrait orientation, the working combination is `w=320, h=240, r=0`.
- `erase()` does **not** reset scroll position or cursor. Always call `reset_scroll()` and `set_pos()` after `erase()`, or new text will appear in the wrong place.
- `set_pos(2, 5)` is the cleanest starting position — anything closer to y=0 clips the top of the first line.

### Standard boilerplate for any new script

```python
from machine import Pin, SPI
from ili934 import ILI9341, color565

backlight = Pin(21, Pin.OUT)
backlight.value(1)

spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

dummy_rst = Pin(4, Pin.OUT)
dummy_rst.value(1)

display = ILI9341(spi, cs=Pin(15), dc=Pin(2), rst=dummy_rst, w=320, h=240, r=0)

display.set_color(color565(0, 0, 0), color565(255, 255, 255))  # black text, white bg
display.erase()
display.reset_scroll()
display.set_pos(2, 5)

display.print("Hello World!")
```

## Folder structure

- `hello_world_and_loops/` — first working scripts: basic text display and a loop test to check how many lines fit on screen / how scrolling behaves.
