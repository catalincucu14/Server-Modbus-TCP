def bytes_to_word(bytes_param: list) -> int:
    """
    Function used to merge to bytes into one, NOT ADDITION, [0x10, 0xA2] -> 0x10A2
    :param bytes_param: self explanatory
    :return: self explanatory
    """

    return (bytes_param[0] << 8) + bytes_param[1]


def int_to_bytes(offset: int, number: int, dimension: int) -> bytes:
    """
    Function used split an int into bytes, 0x04 -> [0x00, 0x04]
    :param offset: an offset
    :param number: the number
    :param dimension: the number of bytes, 2
    :return: self explanatory
    """

    return (offset + number).to_bytes(dimension, 'big')


def bits_to_bytes(bits_param):
    """
    Function used to merge bits (0, 1) into bytes

    :param bits_param: self explanatory
    :return: self explanatory
    """

    pairs = []
    result = []
    byte = 0

    for _ in range(int(len(bits_param) / 8)):
        pairs.append(bits_param[byte:byte + 8][::-1])
        byte = byte + 8

    for i in pairs:
        map_temp = map(int, i)
        n = int(''.join(map(str, map_temp)), 2)
        result.append(int('{:02x}'.format(n), 16))

    return bytes(result)


def bytes_to_bits(register):
    """
    Function used to split a byte into bits

    :param register: self explanatory
    :return: self explanatory
    """

    string = list("{0:b}".format(register).zfill(8))
    list_temp = []

    for i in range(8):
        list_temp.append(ord(string[i]) - ord('0'))

    return list_temp[::-1]
