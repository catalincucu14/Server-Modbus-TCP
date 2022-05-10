import socket

from Source.Modbus.ModbusException import *
from Source.Storage.Database import Database
from Source.Storage.Json import Json
from Source.Utils import *


class Modbus:
    def __init__(self, storage: (Json, Database)):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__storage = storage

    def bind(self, host: str, port: int) -> None:
        """
        Function used to call bind function from the socket

        :param host: self explanatory
        :param port: self explanatory
        :return: None
        """

        self.__socket.bind((host, port))

    def listen(self, dimension: int) -> None:
        """
        Function used to call listen function from the socket

        :param dimension: the most clients it can handle at once
        :return: None
        """

        self.__socket.listen(dimension)

    def accept(self) -> socket:
        """
        Function used to call accept function from the socket

        :return: the socket got from the client
        """

        return self.__socket.accept()

    def close(self) -> None:
        """
        Function used to call close function from the socket

        :return: None
        """

        self.__socket.close()

    def receive(self, connection: socket, address: any) -> None:
        """
        Function used to receive a message from another socket using the given connection

        :param connection: the connection the "client"
        :param address: ip address of the client and the port, tuple usually
        :return: None
        """
        with connection:
            while True:
                message = connection.recv(1024)

                if not message:
                    print(f"[DISCONNECTED FROM {address[0]}]\n")
                    break
                else:
                    print(f"[CONNECTED BY {address[0]}]\n")

                # Create the request message
                request = ADU(message)

                # Generate a response
                print(f"<<< [{address[0]}]  {request.print()}")
                respond = self.__respond(request)

                # Send the response
                print(f">>> [{address[0]}]  {respond.print()}\n")
                connection.sendall(respond.join())

            # Close the connection after the message has been sent
            connection.close()

    def __read_coil_status(self, request: ADU) -> ADU:
        """
        Function used to read multiple coils

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (first coil)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the number of coils to be read
        number_of_coils = bytes_to_word(request.DATA[2:4])

        first_coil = start_address + COILS_OFFSET
        last_coil = first_coil + number_of_coils

        coils = []

        for i in range(first_coil, last_coil):
            coils.append(self.__storage.read_coil(i))

        # Add 0s so it can be divided by 8 (1 byte)
        for _ in range(8 - (len(coils) % 8)):
            coils.append(0)

        # Add the length of the response (coils)
        result = bytes([int(len(coils) / 8)])

        # A coil is sizes 1 bit and will convert then to 1 byte
        result = result + bits_to_bytes(coils)

        response.L = int_to_bytes(2, len(result), 2)
        response.DATA = result

        return response

    def __read_discrete_inputs(self, request: ADU) -> ADU:
        """
        Function used to read multiple discrete inputs

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (first discrete input)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the number of discrete inputs to be read
        number_of_di = bytes_to_word(request.DATA[2:4])

        first_di = start_address + DISCRETE_INPUTS_OFFSET
        last_di = first_di + number_of_di

        discrete_inputs = []

        for i in range(first_di, last_di):
            discrete_inputs.append(self.__storage.read_discrete_input(i))

        # Add 0s so it can be divided by 8 (1 byte)
        for _ in range(8 - (len(discrete_inputs) % 8)):
            discrete_inputs.append(0)

        # Add the length of the response (discrete inputs)
        result = bytes([int(len(discrete_inputs) / 8)])

        # A discrete inputs is sizes 1 bit and will convert then to 1 byte
        result = result + bits_to_bytes(discrete_inputs)

        response.L = int_to_bytes(2, len(result), 2)
        response.DATA = result

        return response

    def __read_holding_registers(self, request: ADU) -> ADU:
        """
        Function used to read multiple holding registers

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (first holding register)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the number of holding register to be read
        number_of_hr = bytes_to_word(request.DATA[2:4])

        first_hr = start_address + HOLDING_REGISTERS_OFFSET
        last_hr = first_hr + number_of_hr

        result = bytes([number_of_hr * 2])

        holding_registers = []

        for i in range(first_hr, last_hr):
            holding_registers.append(self.__storage.read_holding_register(i))

        for i in range(len(holding_registers)):
            result = result + int_to_bytes(0, holding_registers[i], 2)

        response.L = int_to_bytes(2, len(result), 2)
        response.DATA = result

        return response

    def __read_input_registers(self, request: ADU) -> ADU:
        """
        Function used to write multiple input registers

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (first coil)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the number of coils to be read
        number_of_ir = bytes_to_word(request.DATA[2:4])

        first_ir = start_address + INPUT_REGISTERS_OFFSET
        last_ir = first_ir + number_of_ir

        result = bytes([number_of_ir * 2])

        input_registers = []

        for i in range(first_ir, last_ir):
            input_registers.append(self.__storage.read_input_register(i))

        for i in range(len(input_registers)):
            result = result + int_to_bytes(0, input_registers[i], 2)

        response.L = int_to_bytes(2, len(result), 2)
        response.DATA = result

        return response

    def __force_single_coil(self, request: ADU) -> ADU:
        """
        Function used to write one coil

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (coil)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the value to be inserted
        value = bytes_to_word(request.DATA[2:4])

        address_coil = start_address + COILS_OFFSET

        if value == 0xFF00:
            self.__storage.write_coil(1, address_coil)
        elif value == 0x0000:
            self.__storage.write_coil(0, address_coil)

        return response

    def __write_single_register(self, request: ADU) -> ADU:
        """
        Function used to write one holding register

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (holding register)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the value to be inserted
        value = bytes_to_word(request.DATA[2:4])

        address_hr = start_address + HOLDING_REGISTERS_OFFSET

        self.__storage.write_holding_register(value, address_hr)

        return response

    def __force_multiple_coils(self, request: ADU) -> ADU:
        """
        Function used to write multiple coils

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (first coil)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the number of coils to be inserted
        no_coils = bytes_to_word(request.DATA[2:4])

        # Get the number of bytes to be read from the message
        bytes_after = request.DATA[4]

        first_coil = start_address + COILS_OFFSET

        registers = []
        coils = []

        # Get the bytes from the message
        for i in range(5, 5 + bytes_after):
            registers.append(request.DATA[i])

        for i in range(len(registers)):
            coils = coils + (bytes_to_bits(registers[i]))

        for i in range(no_coils):
            self.__storage.write_coil(coils[i], first_coil + i)

        response.L = int_to_bytes(2, 4, 2)
        response.DATA = request.DATA[0:4]

        return response

    def __write_multiple_registers(self, request: ADU) -> ADU:
        """
        Function used to write multiple holding registers

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        response = copy.deepcopy(request)

        # Get the starting address (first holding register)
        start_address = bytes_to_word(request.DATA[0:2])

        # Get the number of holding register to be inserted
        no_hr = bytes_to_word(request.DATA[2:4])

        # Get the number of bytes to be read from the message
        bytes_after = request.DATA[4]

        first_hr = start_address + HOLDING_REGISTERS_OFFSET
        holding_registers = []

        for i in range(5, 5 + bytes_after):
            holding_registers.append(request.DATA[i])

        for i in range(no_hr):
            bytes_hr = bytes_to_word(holding_registers[(i * 2):(i * 2 + 2)])
            self.__storage.write_holding_register(bytes_hr, first_hr + i)

        response.L = int_to_bytes(2, 4, 2)
        response.DATA = request.DATA[0:4]

        return response

    def __respond(self, request: ADU) -> ADU:
        """
        Based on the function code (FC) calls that function

        :param request: the request to be processed
        :return: the response made from the request with DATA and L modified
        """

        # Check for exceptions
        exception = ModbusException.check(request)

        if exception is None:
            return {
                0x01: self.__read_coil_status,
                0x02: self.__read_discrete_inputs,
                0x03: self.__read_holding_registers,
                0x04: self.__read_input_registers,
                0x05: self.__force_single_coil,
                0x06: self.__write_single_register,
                0x0F: self.__force_multiple_coils,
                0x10: self.__write_multiple_registers,
            }[request.FC[0]](request)
        else:
            return exception
