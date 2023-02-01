import base64
from Crypto.Cipher import AES
from Crypto import Random


def encrypt(key, source, encode=True, key_type='hex'):
    """
    :param key: hex or ascii, will be converted to bytes
    :param source: what you want to encrypt
    :param encode: base64 (else not implemented)
    :param key_type: hex or ascii
    :return: base64 (when default) encoded source
    """

    source = source.encode()
    if key_type == "hex":
        key = bytes(bytearray.fromhex(key))
    # else not implemented

    # initialization_vector is an arbitrary number that can be used with
    # a secret key for data encryption
    initialization_vector = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, initialization_vector)

    # padding is any of a number of distinct practices which all include
    # adding data to the beginning, middle, or end of a message
    # prior to encryption
    padding = AES.block_size - len(
        source) % AES.block_size
    source += bytes(
        [padding]) * padding

    # initialization vector is placed at the beginning
    # and then encrypted source
    data = initialization_vector + encryptor.encrypt(
        source)

    return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True, key_type="hex"):
    """
    :param key: ascii or hex. Key necessary to decrypt
    :param source: the encrypted message or password to decrypt
    :param decode: if true, base64 decode is necessary before key decryption
    :param key_type: default hex, else not implemented
    :return: the decrypted source
    """

    source = source.encode()
    if decode:
        source = base64.b64decode(source)

    # from hex to bytes
    if key_type == "hex":
        key = bytes(bytearray.fromhex(key))

    # extract initialization_vector
    initialization_vector = source[:AES.block_size]

    decryption = AES.new(key, AES.MODE_CBC, initialization_vector)
    # decrypt
    data = decryption.decrypt(source[AES.block_size:])

    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("That padding value is not valid.")
    return data[:-padding]
