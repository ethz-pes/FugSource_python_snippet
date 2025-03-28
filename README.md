# Python Code for FuG Elektronik Power Sources (Ethernet)

![license - BSD](https://img.shields.io/badge/license-BSD-green)
![language - python](https://img.shields.io/badge/language-python-blue)
![category - power electronics](https://img.shields.io/badge/category-power%20electronics-lightgrey)
![status - unmaintained](https://img.shields.io/badge/status-unmaintained-red)

This **Python** class remote control power sources from **FuG Elektronik GmbH** over ethernet:
* connect to the device
* enable/disable the power source
* set the voltage and the current limit
* read the voltage and the current values

This class:
* was tested on "MS Windows" but should run with Linux
* was tested with Python 3.6 but should run with Python 3.x

The following FuG power sources were tested:
* "FuG HYN" (at ETH Zurich)
* "FuG HCP" (at ETH Zurich)
* "FuG MCP" (at Leibniz Hannover University)

This class is meant as a lightweight code to be used as a "code snippet" and not as a full package.
Power sources are dangerous and Python does not qualify as an high-integrity programming language.
External safety circuits (such as breakers) are required to guarantee the absence of hazards.

## Author

* **Thomas Guillod, ETH Zurich, Power Electronic Systems Laboratory** - [GitHub Profile](https://github.com/otvam)

## License

* This project is licensed under the **BSD License**, see [LICENSE.md](LICENSE.md).
* This project is copyrighted by: (c) 2020-2021, ETH Zurich, Power Electronic Systems Laboratory, T. Guillod.
