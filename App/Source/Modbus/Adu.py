from Source.Utils import bytes_to_word


class ADU:
    def __init__(self, request):
        self.TI = request[0:2]
        self.PI = request[2:4]
        self.L = request[4:6]
        self.UI = request[6:7]
        self.FC = request[7:8]
        self.DATA = request[8:6 + bytes_to_word(self.L)]

    def join(self) -> bytes:
        """
        Function used to make merge the ADU into a list of bytes

        :return: self explanatory
        """
        return self.TI + self.PI + self.L + self.UI + self.FC + self.DATA

    def print(self):
        """
        Function used to get a string with ADU representation

        :return: self explanatory
        """

        string = format(self.TI[0], '#04X')[2:] + \
                 format(self.TI[1], '#04X')[2:] + " " + \
                 format(self.PI[0], '#04X')[2:] + \
                 format(self.PI[1], '#04X')[2:] + " " + \
                 format(self.L[0], '#04X')[2:] + \
                 format(self.L[1], '#04X')[2:] + " " + \
                 format(self.UI[0], '#04X')[2:] + " " + \
                 format(self.FC[0], '#04X')[2:] + " "

        for i in range(len(self.DATA)):
            string = string + format(self.DATA[i], '#04X')[2:]

        return string
