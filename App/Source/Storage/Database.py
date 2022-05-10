import mysql.connector

from Source.Config import *


class Database:
    def __init__(self, host: str, user: str, password: str):
        self.__connection = mysql.connector.connect(host=host, user=user, password=password)

        cursor = self.__connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ModbusTCP")

        self.__connection = mysql.connector.connect(host=host, user=user, password=password, database="ModbusTCP")
        self.__create_tables()
        self.__initialize_tables()

    def __create_tables(self) -> None:
        """
        Function used to create the tables

        :return: None
        """

        cursor = self.__connection.cursor()

        tables = ["CREATE TABLE IF NOT EXISTS Coils(ID SMALLINT PRIMARY KEY, VALUE BOOLEAN)",
                  "CREATE TABLE IF NOT EXISTS DiscreteInputs(ID INT PRIMARY KEY, VALUE BOOLEAN)",
                  "CREATE TABLE IF NOT EXISTS InputRegisters(ID INT PRIMARY KEY, VALUE SMALLINT UNSIGNED)",
                  "CREATE TABLE IF NOT EXISTS HoldingRegisters(ID INT PRIMARY KEY, VALUE SMALLINT UNSIGNED)"]

        # Create the database with the tables for all 4 types of data
        if self.__connection is not None:
            for Table in tables:
                try:
                    cursor.execute(Table)
                except Exception as e:
                    print(e)

    def __initialize_tables(self) -> None:
        """
        Function used to initialize the tables, all values are 0

        :return: None
        """

        cursor = self.__connection.cursor()

        for i in range(COILS_OFFSET + 1, 250):
            cursor.execute(f"INSERT IGNORE INTO Coils(ID, VALUE) VALUES ({i}, 0)")

        for i in range(DISCRETE_INPUTS_OFFSET + 1, 10250):
            cursor.execute(f"INSERT IGNORE INTO DiscreteInputs(ID, VALUE) VALUES ({i}, 0)")

        for i in range(INPUT_REGISTERS_OFFSET + 1, 30250):
            cursor.execute(f"INSERT IGNORE INTO InputRegisters(ID, VALUE) VALUES ({i}, 0)")

        for i in range(HOLDING_REGISTERS_OFFSET + 1, 40250):
            cursor.execute(f"INSERT IGNORE INTO HoldingRegisters(ID, VALUE) VALUES ({i}, 0)")

        self.__connection.commit()

    def reset_coils(self) -> None:
        """
        Function used to reset the coils

        :return: None
        """

        cursor = self.__connection.cursor()

        for i in range(1, 250):
            cursor.execute("UPDATE Coils SET VALUE = %s WHERE ID = %s", (0, i))

        self.__connection.commit()

    def reset_discrete_inputs(self) -> None:
        """
        Function used to reset the discrete inputs

        :return: None
        """

        cursor = self.__connection.cursor()

        for i in range(10001, 10250):
            cursor.execute("UPDATE DiscreteInputs SET VALUE = %s WHERE ID = %s", (0, i))

        self.__connection.commit()

    def reset_input_registers(self) -> None:
        """
        Function used to reset the input registers

        :return: None
        """

        cursor = self.__connection.cursor()

        for i in range(30001, 30250):
            cursor.execute("UPDATE InputRegisters SET VALUE = %s WHERE ID = %s", (0, i))

        self.__connection.commit()

    def reset_holding_registers(self) -> None:
        """
        Function used to reset the holding registers

        :return: None
        """

        cursor = self.__connection.cursor()

        for i in range(40001, 40250):
            cursor.execute("UPDATE HoldingRegisters SET VALUE = %s WHERE ID = %s", (0, i))

        self.__connection.commit()

    def read_coil(self, address: int) -> int:
        """
        Function used to read a coil

        :param address: the address of the coil
        :return: the value of the coil
        """

        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT VALUE FROM Coils WHERE ID = {address}")
        return cursor.fetchall()[0][0]

    def read_discrete_input(self, address: int) -> int:
        """
        Function used to read a discrete input

        :param address: the address of the discrete input
        :return: the value of the discrete input
        """

        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT VALUE FROM DiscreteInputs WHERE ID = {address}")
        return cursor.fetchall()[0][0]

    def read_holding_register(self, address: int) -> int:
        """
        Function used to read a holding register

        :param address: the address of the holding register
        :return: the value of the holding register
        """

        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT VALUE FROM HoldingRegisters WHERE ID = {address}")
        return cursor.fetchall()[0][0]

    def read_input_register(self, address: int) -> int:
        """
        Function used to read an input register

        :param address: the address of the input register
        :return: the value of the input register
        """

        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT VALUE FROM InputRegisters WHERE ID = {address}")
        return cursor.fetchall()[0][0]

    def write_coil(self, value: int, address: int) -> None:
        """
        Function used to write a coil

        :param value: value of the coil
        :param address: the address of the coil
        :return: None
        """

        cursor = self.__connection.cursor()
        cursor.execute(f"UPDATE Coils SET VALUE = {value} WHERE ID = {address}")
        self.__connection.commit()

    def write_holding_register(self, value: int, address: int) -> None:
        """
        Function used to write a holding register

        :param value: value of the holding register
        :param address: the address of the holding register
        :return: None
        """

        cursor = self.__connection.cursor()
        cursor.execute(f"UPDATE HoldingRegisters SET VALUE = {value} WHERE ID = {address}")
        self.__connection.commit()
