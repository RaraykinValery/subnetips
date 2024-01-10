# На вход подаётся IP с указанием маски подсети по CIDR
# Например: 192.168.5.20/24
# Программа определяет:
# - подсеть
# - первый IP в подсети
# - последний IP в подсети
# - broadcast IP для подсети
# Дополнительно интересно было бы определить:
# - сколько всего IP адресов в подсети
# - входит ли данный IP в данную подсеть
# - разбить сеть на подсети с заданным колвом хостов

import sys
from bitarray import bitarray
import ip_conv


class IP:
    def __init__(self, ip: str, mask: str = "") -> None:
        self.ip_str: str = ip
        self.mask: str = mask
        self.intoctets: list[int] = ip_conv.str2intoc(ip)
        self.boctets: list[bitarray] = ip_conv.intoc2boc(self.intoctets)
        self.bits: bitarray = ip_conv.boc2bits(self.boctets)

    def __repr__(self):
        repr: str = self.ip_str
        if self.mask:
            repr += "/" + self.mask

        return repr


class SubnetCalculator:
    def __init__(self, ip: IP, mask: str) -> None:
        self.ip: IP = ip
        self.mask: int = int(mask)

    def create_ip(self):
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 0
        created_ip: IP = IP(ip_conv.bits2strip(ip_bits), str(self.mask))

        return created_ip

    @property
    def subnet_ip(self) -> IP:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 0
        subnet_ip: IP = IP(ip_conv.bits2strip(ip_bits), str(self.mask))

        return subnet_ip

    @property
    def first_ip(self) -> list[int]:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 0
        ip_bits[-1] = 1
        first_ip: IP = IP(ip_conv.bits2strip(ip_bits), str(self.mask))

        return first_ip

    @property
    def last_ip(self) -> list[int]:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 1
        ip_bits[-1] = 0
        last_ip: IP = IP(ip_conv.bits2strip(ip_bits), str(self.mask))

        return last_ip

    @property
    def broadcast_ip(self) -> list[int]:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 1
        broadcast_ip: IP = IP(ip_conv.bits2strip(ip_bits), str(self.mask))

        return broadcast_ip

    @property
    def ips_number(self) -> int:
        pass


if __name__ == "__main__":
    print(sys.argv[1])

    ip_str: str
    mask_str: str

    ip_str, mask_str = sys.argv[1].split("/")

    ip: IP = IP(ip_str, mask_str)

    subnet_calculator = SubnetCalculator(ip, mask_str)
    print(subnet_calculator.subnet_ip)
    print(subnet_calculator.first_ip)
    print(subnet_calculator.last_ip)
    print(subnet_calculator.broadcast_ip)

    subnet_calculator.mask = 11
    print(subnet_calculator.subnet_ip)
    print(subnet_calculator.first_ip)
    print(subnet_calculator.last_ip)
    print(subnet_calculator.broadcast_ip)
