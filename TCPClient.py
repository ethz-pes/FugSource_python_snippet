import socket


class TCPClient():
    """
    Class for communicating with the FuG power source over TCP/IP.
    """

    def __init__(self, data):
        """
        Constructor of the TCPClient class.
        """

        self.data = data
        self.link = None
        self.data_buffer = ''

    def open(self):
        """
        Connect to the power source and set the timeout of the connection.
        """

        self.link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.link.connect((self.data["ip"], self.data["port"]))
        self.link.settimeout(self.data["timeout"])

    def close(self):
        """
        Close the connection.
        """

        self.data_buffer = ''
        self.link.close()
        self.link = None

    def start_command(self):
        """
        Clear the buffer for starting a new command.
        """

        self._receive_bytes()
        self.data_buffer = ''

    def send_byte(self, msg):
        """
        Send a byte to the power source.
        """

        try:
            self.link.send(msg)
        except Exception:
            raise ValueError("send fail")

    def receive(self):
        """
        Get responses from the power source where the newline is the delimiter.
        """

        response = []
        buffer_new = self._receive_bytes()
        for char in buffer_new:
            if char == '\n':
                response.append(self.data_buffer)
                self.data_buffer = ''
            else:
                self.data_buffer += char

        return response

    def _receive_bytes(self):
        """
        Get bytes from the power sources.
        """

        try:
            try:
                return self.link.recv(self.data["buffer"])
            except socket.timeout:
                return ''
        except Exception:
            raise ValueError("receive fail")
