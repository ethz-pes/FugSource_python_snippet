import FugSource


if __name__ == "__main__":
    """
    Test code for the FugSource class.
    """

    # create the object
    data = dict()
    data["ip"] = "xxx.xx.xx.x"
    data["port"] = 2101
    data["timeout"] = 0.01
    data["buffer"] = 1024
    data["delay_send"] = 0.01
    data["delay_wait"] = 1.0
    data["delay_loop"] = 0.01
    obj = FugSource.FugSource(data)

    # connect to the device
    obj.open()

    # enable the voltage source
    obj.enable()

    # set the current limit
    obj.set_I(0.5)

    # set the voltage
    obj.set_I(800)

    # read the voltage and current
    value = obj.get_V()
    value = obj.get_I()

    # disable the voltage source
    obj.disable()

    # disconnect from the device
    obj.close()
