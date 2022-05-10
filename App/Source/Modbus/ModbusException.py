import copy
from typing import Optional

from Source.Config import *
from Source.Modbus.Adu import ADU
from Source.Utils import *


class ModbusException:
    @staticmethod
    def __illegal_function(request) -> Optional[ADU]:
        """
        Function used to check if the modbus function code is correct

        :param request: the request made by the client
        :return: exception response or None if everything is ok
        """

        function = request.FC[0]

        if function in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10]:
            return None
        else:
            response = copy.deepcopy(request)

            response.FC = bytes([response.FC[0] + 0x80])
            response.DATA = bytes([ILLEGAL_FUNCTION])

            return response

    @staticmethod
    def __illegal_data_address(request) -> Optional[ADU]:
        """
        Function used to check if the address is correct, starting address and finish address

        :param request: the request made by the client
        :return: exception response or None if everything is ok
        """

        function = request.FC[0]

        if function in [0x01, 0x02, 0x03, 0x04, 0x0F, 0x10]:
            start_address = bytes_to_word(request.DATA[0:2])
            number_of_data = bytes_to_word(request.DATA[2:4])

            if (0x01 <= start_address <= 0xF9) and (0x01 <= (start_address + number_of_data - 1) <= 0xF9):
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_ADDRESS])

                return response

        if function in [0x05, 0x06]:
            start_address = bytes_to_word(request.DATA[0:2])

            if 0x01 <= start_address <= 0xF9:
                return None
            else:
                response = copy.deepcopy(request)
                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_ADDRESS])
                return response

    @staticmethod
    def __illegal_data_value(request) -> Optional[ADU]:
        """
        Function used to check if the values given in the request are valid, read more in the documentation

        :param request: the request made by the client
        :return: exception response or None if everything is ok
        """

        function = request.FC[0]

        if function in [0x01, 0x02]:
            quantity = bytes_to_word(request.DATA[2:4])

            if 0x01 <= quantity <= 0xF9:
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_VALUE])

                return response

        if function in [0x03, 0x04]:
            quantity = bytes_to_word(request.DATA[2:4])

            if 0x01 <= quantity <= 0x7D:
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_VALUE])

                return response

        if function == 0x05:
            value = bytes_to_word(request.DATA[2:4])

            if value in [0x0000, 0xFF00]:
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_VALUE])

                return response

        if function == 0x06:
            value = bytes_to_word(request.DATA[2:4])

            if 0x0000 <= value <= 0xFFFF:
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_VALUE])

                return response

        if function == 0x0F:
            quantity = bytes_to_word(request.DATA[2:4])
            bytes_after = request.DATA[4]

            if (0x01 <= quantity <= 0xF9) and (bytes_after == (int(quantity / 8) + (quantity % 8 > 0))):
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_VALUE])

                return response

        if function == 0x10:
            quantity = bytes_to_word(request.DATA[2:4])
            bytes_after = request.DATA[4]

            if (0x01 <= quantity <= 0x7B) and (bytes_after == quantity * 2):
                return None
            else:
                response = copy.deepcopy(request)

                response.FC = bytes([response.FC[0] + 0x80])
                response.DATA = bytes([ILLEGAL_DATA_VALUE])

                return response

    @staticmethod
    def check(request) -> Optional[ADU]:
        """
        Function used to check if

        :param request: the request made by the client
        :return: exception response or None if everything is ok
        """

        exception = ModbusException.__illegal_function(request)
        if exception is not None:
            return exception

        exception = ModbusException.__illegal_data_address(request)
        if exception is not None:
            return exception

        exception = ModbusException.__illegal_data_value(request)
        if exception is not None:
            return exception

        return None
