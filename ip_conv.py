from bitarray import bitarray, util


def str2intoc(ip: str) -> list[int]:
    return list(map(lambda x: int(x), ip.split(".")))


def intoc2str(ip_intoctets: list[int]) -> str:
    return ".".join(list(map(lambda x: str(x), ip_intoctets)))


def intoc2boc(ip_intoctets: list[int]) -> list[bitarray]:
    return list(
        map(lambda x: util.int2ba(x, length=8), ip_intoctets)
    )


def boc2intoc(ip_octets: list[bitarray]) -> list[int]:
    return list(map(lambda x: util.ba2int(x), ip_octets))


def boc2bits(bytes_list: list[bitarray]):
    ip_bits: bitarray = bitarray()

    for part in bytes_list:
        ip_bits += part

    return ip_bits


def bits2boc(ip_bits: bitarray) -> list[bitarray]:
    ip_bytes: list[bitarray] = []
    for i in range(len(ip_bits) // 8):
        ip_bytes.append(ip_bits[i*8:i*8 + 8])

    return ip_bytes


def bits2strip(ip_bits: bitarray) -> str:
    return intoc2str(boc2intoc(bits2boc(ip_bits)))
