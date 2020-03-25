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

* Adafruit PCT2075 Breakout: https://www.adafruit.com/products/4369

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases



* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit
import adafruit_bus_device.i2c_device as i2cdevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCT2075.git"
# pylint: disable=bad-whitespace, too-few-public-methods
PCT2075_DEFAULT_ADDRESS = 0x37  # Address is configured with pins A0-A2

PCT2075_REGISTER_TEMP = 0  # Temperature register (read-only)
PCT2075_REGISTER_CONFIG = 1  # Configuration register
PCT2075_REGISTER_THYST = 2  # Hysterisis register
PCT2075_REGISTER_TOS = 3  # OS register
PCT2075_REGISTER_TIDLE = 4  # Measurement idle time register


class Mode:
    """Options for `mode`"""

    INTERRUPT = 1
    COMPARITOR = 0


class FaultCount:
    """Options for `faults_to_alert`"""

    FAULT_1 = 0
    FAULT_2 = 1
    FAULT_4 = 2
    FAULT_6 = 3


# pylint: enable=bad-whitespace, too-few-public-methods


class PCT2075:
    """Driver for the PCT2075 Digital Temperature Sensor and Thermal Watchdog.
        :param ~busio.I2C i2c_bus: The I2C bus the PCT2075 is connected to.
        :param address: The I2C device address for the sensor. Default is ``0x37``.
    """

    def __init__(self, i2c_bus, address=PCT2075_DEFAULT_ADDRESS):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)

    _temperature = ROUnaryStruct(PCT2075_REGISTER_TEMP, ">h")
    mode = RWBit(PCT2075_REGISTER_CONFIG, 1, register_width=1)
    """Sets the alert mode. In comparitor mode, the sensor acts like a thermostat and will activate
    the INT pin according to `high_temp_active_high` when an alert is triggered. The INT pin will be
    deactiveated when the temperature falls below `temperature_hysteresis`. In interrupt mode the
    INT pin is activated once when a temperature fault is detected, and once more when the
    temperature falls below `temperature_hysteresis`. In interrupt mode, the alert is cleared by
    reading a property"""

    shutdown = RWBit(PCT2075_REGISTER_CONFIG, 0, 1)
    """Set to True to turn off the temperature measurement circuitry in the sensor. While shut down
    the configurations properties can still be read or written but the temperature will not be
    measured"""
    _fault_queue_length = RWBits(2, PCT2075_REGISTER_CONFIG, 3, register_width=1)
    _high_temperature_threshold = UnaryStruct(PCT2075_REGISTER_TOS, ">h")
    _temp_hysteresis = UnaryStruct(PCT2075_REGISTER_THYST, ">h")
    _idle_time = RWBits(5, PCT2075_REGISTER_TIDLE, 0, register_width=1)
    high_temp_active_high = RWBit(PCT2075_REGISTER_CONFIG, 2, register_width=1)
    """Sets the alert polarity. When False the INT pin will be tied to ground when an alert is
    triggered. If set to True it will be disconnected from ground when an alert is triggered."""

    @property
    def temperature(self):
        """Returns the current temperature in degress celsius. Resolution is 0.125 degrees C"""
        return (self._temperature >> 5) * 0.125

    @property
    def high_temperature_threshold(self):
        """The temperature in degrees celsius that will trigger an alert on the INT pin if it is
        exceeded. Resolution is 0.5 degrees C."""
        return (self._high_temperature_threshold >> 7) * 0.5

    @high_temperature_threshold.setter
    def high_temperature_threshold(self, value):
        self._high_temperature_threshold = int(value * 2) << 7

    @property
    def temperature_hysteresis(self):
        """The temperature hysteresis value defines the bottom of the temperature range in degrees
        C in which the temperature is still considered high". `temperature_hysteresis` must be
        lower than `high_temperature_threshold`. Resolution is 0.5 degrees C.
        """
        return (self._temp_hysteresis >> 7) * 0.5

    @temperature_hysteresis.setter
    def temperature_hysteresis(self, value):
        if value >= self.high_temperature_threshold:
            raise ValueError(
                "temperature_hysteresis must be less than high_temperature_threshold"
            )
        self._temp_hysteresis = int(value * 2) << 7

    @property
    def faults_to_alert(self):
        """The number of consecutive high temperature faults required to raise an alert. An fault
        is tripped each time the sensor measures the temperature to be greater than
        `high_temperature_threshold`. The rate at which the sensor measures the temperature
        is defined by `delay_between_measurements`.
        """

        return self._fault_queue_length

    @faults_to_alert.setter
    def faults_to_alert(self, value):
        if value > 4 or value < 1:
            raise ValueError("faults_to_alert must be an adafruit_pct2075.FaultCount")
        self._fault_queue_length = value

    @property
    def delay_between_measurements(self):
        """The amount of time between measurements made by the sensor in milliseconds. The value
        must be between 100 and 3100 and a multiple of 100"""
        return self._idle_time * 100

    @delay_between_measurements.setter
    def delay_between_measurements(self, value):
        if value > 3100 or value < 100 or value % 100 > 0:
            raise AttributeError(
                """"delay_between_measurements must be >= 100 or <= 3100\
            and a multiple of 100"""
            )
        self._idle_time = int(value / 100)
