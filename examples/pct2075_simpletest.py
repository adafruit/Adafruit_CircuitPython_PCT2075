# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_pct2075

i2c = board.I2C()
pct = adafruit_pct2075.PCT2075(i2c)

while True:
    print("Temperature: %.2f C" % pct.temperature)
    time.sleep(0.5)
