Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-pct2075/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/pct2075/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_PCT2075/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_PCT2075/actions/
    :alt: Build Status

CircuitPython library for the `NXP PCT2075`_ Digital Temperature Sensor

Also supports the Microchip TC74_

.. _NXP PCT2075: https://www.adafruit.com/product/4369
.. _TC74: https://www.adafruit.com/product/4375

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-pct2075/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-pct2075

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-pct2075

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-pct2075

Usage Example
=============

.. code-block:: python

    import time
    import board
    import busio
    import adafruit_pct2075
    i2c = busio.I2C(board.SCL, board.SDA)

    pct = adafruit_pct2075.PCT2075(i2c)

    while True:
        print("Temperature: %.2f C"%pct.temperature)
        time.sleep(0.5)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_PCT2075/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
