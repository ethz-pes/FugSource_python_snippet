# (c) 2020, ETH Zurich, Power Electronic Systems Laboratory, T. Guillod

import time
import TCPClient


class FugSource():
    """
    This Python class remote control power sources from "FuG Elektronik GmbH" over ethernet:
        - connect to the device
        - enable/disable the power source
        - set the voltage and the current limit
        - read the voltage and the current values

    This class:
        - works with the "FuG HYN" and "FuG HCP"
        - was tested on "MS Windows" but should run with Linux
        - was tested with Python 2.7 but should run with Python 3.x

    This class is meant as a lightweight code to be used as a "code snippet" and not as a full package.
    Power sources are dangerous and Python does not qualify as an high-integrity programming language.
    External safety circuits (such as breakers) are required to guarantee the absence of hazards.
    """

    def __init__(self, data):
        """
        Constructor of the FugSource class.
        """

        self.data = data
        self.TCPClient_obj = TCPClient.TCPClient(self.data)
        self.V = None
        self.I = None

    def open(self):
        """
        Connect to the power source.
        """

        self.TCPClient_obj.open()

    def close(self):
        """
        Disconnect from the power source.
        """

        self.V = None
        self.I = None
        self.TCPClient_obj.close()

    def enable(self):
        """
        Enable the power source (with zero voltage/current).
        """

        self.set_V(0.0)
        self.set_I(0.0)
        self._send_command(["enable"], None)
        self._wait_response(["ack"])

    def disable(self):
        """
        Disable the power source (reset the voltage/current to zero).
        """

        self.set_V(0.0)
        self.set_I(0.0)
        self._send_command(["disable"], None)
        self._wait_response(["ack"])

    def set_V(self, V):
        """
        Set the voltage level.
        """

        self._send_command(["set_V"], V)
        self._wait_response(["ack"])

    def set_I(self, I):
        """
        Set the current limit.
        """

        self._send_command(["set_I"], I)
        self._wait_response(["ack"])

    def get_V(self):
        """
        Read the measured voltage level.
        """

        self._send_command(["get_V", "wait"], None)
        self._wait_response(["ack", "V"])
        return self.V

    def get_I(self):
        """
        Read the measured current level.
        """

        self._send_command(["get_I", "wait"], None)
        self._wait_response(["ack", "I"])
        return self.I

    def _send_command(self, send, data):
        """
        Send a command to the power source.
        """

        # reset the buffer
        self.TCPClient_obj.start_command()

        # send byte per byte with delay to avoid buffer issues inside the power source
        for send_tmp in send:
            self.TCPClient_obj.send_byte(self._parse_send(send_tmp, data))
            time.sleep(self.data["delay_send"])

    def _parse_send(self, command, data):
        """
        Parse the command to the power source instruction set.
        """

        if command == "enable":
            return 'F1\n'
        elif command == "disable":
            return "F0\n"
        elif command == "set_V":
            return 'U%.0f\n' % data
        elif command == "set_I":
            return 'I%.3f\n' % data
        elif command == "get_V":
            return 'N0\n'
        elif command == "get_I":
            return 'N1\n'
        elif command == "wait":
            return '?\n'
        else:
            raise ValueError("invalid send")

    def _wait_response(self, response_wait):
        """
        Get and parse the responses from the power source.
        """

        # init
        timestamp = time.time()
        is_done = False
        idx = 0

        # try until the time is up or the response is complete
        while ((time.time() - timestamp) < self.data["delay_wait"]) and (is_done is False):
            try:
                # get the responses
                response_list = self.TCPClient_obj.receive()

                # check that the response are the expected one
                for response in response_list:
                    response = self._parse_response(response)
                    if response == response_wait[idx]:
                        if (idx + 1) == len(response_wait):
                            is_done = True
                        else:
                            idx += 1
                    else:
                        raise ValueError("invalid response")

                # polling delay of the loop
                time.sleep(self.data["delay_loop"])
            except Exception as e:
                raise ValueError("connection error")

        # if the timeout is reached
        if is_done is False:
            raise ValueError("command timeout")

    def _parse_response(self, command):
        """
        Parse the responses from the power source and set the data.
        """

        if command == "E0":
            return "ack"
        elif (len(command) == 13) and (command[-2:] == 'VN'):
            self.V = float(command[:11])
            return "V"
        elif (len(command) == 13) and (command[-2:] == 'AN'):
            self.I = float(command[:11])
            return "I"
        else:
            raise ValueError("invalid response")
