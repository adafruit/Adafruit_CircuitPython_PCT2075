# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_pct2075`
================================================================================

CircuitPython library for the NXP PCT2075 Digital Temperature Sensor


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases



* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import RWBit, ROBit
import adafruit_bus_device.i2c_device as i2cdevice
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCT2075.git"

#PCT2075_DEFAULT_ADDRESS		 = 0x37		# Address is configured with pins A0-A2
PCT2075_DEFAULT_ADDRESS		 = 0x48		# Address is configured with pins A0-A2
PCT2075_REGISTER_TEMP		 = 0		# Temperature register (read-only)
PCT2075_REGISTER_CONFIG		 = 1		# Configuration register
PCT2075_REGISTER_THYST		 = 2		# Hysterisis register
PCT2075_REGISTER_TOS		 = 3		# OS register
PCT2075_REGISTER_TIDLE       = 4        # Measurement idle time register

class Mode:
    INTERRUPT = 1
    COMPARITOR = 0

class FaultCount:
    FAULT_1 = 0
    FAULT_2 = 1
    FAULT_4 = 3
    FAULT_6 = 4


class PCT2075:

    def __init__(self, i2c_bus, address=PCT2075_DEFAULT_ADDRESS):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)

    _temperature = ROUnaryStruct(PCT2075_REGISTER_TEMP, ">h")
    mode = RWBit(PCT2075_REGISTER_CONFIG, 1, register_width=1)

    shutdown = RWBit(PCT2075_REGISTER_CONFIG, 0, 1)
    _fault_queue_length = RWBits(2, PCT2075_REGISTER_CONFIG, 5, register_width=1)
    _high_temperature_threshold = UnaryStruct(PCT2075_REGISTER_TOS, ">h")
    _temp_hysteresis = UnaryStruct(PCT2075_REGISTER_THYST, ">h")
    _idle_time = RWBits(5, PCT2075_REGISTER_TIDLE, 0, register_width=1)
    high_temp_active_low = RWBit(PCT2075_REGISTER_CONFIG, 2, register_width=1)

    @property
    def temperature(self):
        """WHAT DO YOU THINK THIS RETURNS?"""
        return (self._temperature>>5) *  0.125

    @property
    def high_temperature_threshold(self):
        return (self._high_temperature_threshold >> 7) * 0.5

    @high_temperature_threshold.setter
    def high_temperature_threshold(self, value):
        self._high_temperature_threshold = (int(value * 2) << 7)

    @property
    def temperature_hysteresis(self):
        return (self._temp_hysteresis  >> 7) * 0.5

    @temperature_hysteresis.setter
    def temperature_hysteresis(self, value):
        # TODO: check that hyst is < threshold
        self._temp_hysteresis = (int(value * 2) << 7)

    @property
    def faults_to_alert(self):
        return self._fault_queue_length

    @faults_to_alert.setter
    def faults_to_alert(self, value):
        if value > 4 or value < 1:
            raise ValueError("faults_to_alert must be an adafruit_pct2075.FaultCount")
        self._fault_queue_length = value
