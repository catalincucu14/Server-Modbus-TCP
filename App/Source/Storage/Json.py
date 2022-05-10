import json

from Source.Config import *


class Json:
    def __init__(self, path: str, create: bool):
        self.path = path
        if create:
            self.generate_json()

    def generate_json(self) -> None:
        """
        Function used to create the json file

        :return: None
        """
        json_temp = {
            "Coils": {},
            "DiscreteInputs": {},
            "InputRegisters": {},
            "HoldingRegisters": {}
        }
        for i in range(COILS_OFFSET + 1, 250):
            json_temp["Coils"][str(i)] = 0

        for i in range(DISCRETE_INPUTS_OFFSET + 1, 10250):
            json_temp["DiscreteInputs"][str(i)] = 0

        for i in range(INPUT_REGISTERS_OFFSET + 1, 30250):
            json_temp["InputRegisters"][str(i)] = 0

        for i in range(HOLDING_REGISTERS_OFFSET + 1, 40250):
            json_temp["HoldingRegisters"][str(i)] = 0

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))

    def reset_coils(self) -> None:
        """
        Function used to reset the coils

        :return: None
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        for i in range(COILS_OFFSET + 1, 250):
            json_temp["Coils"][str(i)] = 0

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))

    def reset_discrete_inputs(self) -> None:
        """
        Function used to reset the discrete inputs

        :return: None
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        for i in range(DISCRETE_INPUTS_OFFSET + 1, 10250):
            json_temp["DiscreteInputs"][str(i)] = 0

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))

    def reset_input_registers(self) -> None:
        """
        Function used to reset the input registers

        :return: None
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        for i in range(INPUT_REGISTERS_OFFSET + 1, 30250):
            json_temp["InputRegisters"][str(i)] = 0

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))

    def reset_holding_registers(self) -> None:
        """
        Function used to reset the holding registers

        :return: None
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        for i in range(HOLDING_REGISTERS_OFFSET + 1, 40250):
            json_temp["HoldingRegisters"][str(i)] = 0

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))

    def read_coil(self, address: int) -> int:
        """
        Function used to read a coil

        :param address: the address of the coil
        :return: the value of the coil
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        return json_temp["Coils"][str(address)]

    def read_discrete_input(self, address: int) -> int:
        """
        Function used to read a discrete input

        :param address: the address of the discrete input
        :return: the value of the discrete input
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        return json_temp["DiscreteInputs"][str(address)]

    def read_holding_register(self, address: int) -> int:
        """
        Function used to read a holding register

        :param address: the address of the holding register
        :return: the value of the holding register
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        return json_temp["HoldingRegisters"][str(address)]

    def read_input_register(self, address: int) -> int:
        """
        Function used to read an input register

        :param address: the address of the input register
        :return: the value of the input register
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        return json_temp["InputRegisters"][str(address)]

    def write_coil(self, value: int, address: int) -> None:
        """
        Function used to write a coil

        :param value: value of the coil
        :param address: the address of the coil
        :return: None
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        json_temp["Coils"][str(address)] = value

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))

    def write_holding_register(self, value: int, address: int) -> None:
        """
        Function used to write a holding register

        :param value:  value of the holding register
        :param address: the address of the holding register
        :return: None
        """

        with open(self.path, "r") as file:
            json_temp = json.loads(file.read())

        json_temp["HoldingRegisters"][str(address)] = value

        with open(self.path, "w+") as file:
            file.write(json.dumps(json_temp))
