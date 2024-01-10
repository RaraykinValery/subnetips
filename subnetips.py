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
    def __init__(self, ip: str) -> None:
        self.ip_str: str = ip
        self.intoctets: list[int] = ip_conv.str2intoc(ip)
        self.boctets: list[bitarray] = ip_conv.intoc2boc(self.intoctets)
        self.bits: bitarray = ip_conv.boc2bits(self.boctets)


class SubnetCalculator:
    def __init__(self, ip: IP, mask: str) -> None:
        self.ip: IP = ip
        self.mask: int = int(mask)

    @property
    def subnet_ip(self) -> str:
        subnet_bits: bitarray = self.ip.bits
        subnet_bits[self.mask:] = 0
        subnet_ip: str = ip_conv.bits2strip(subnet_bits)

        return subnet_ip

    @property
    def first_ip(self) -> str:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 0
        ip_bits[-1] = 1

        return ip_conv.bits2strip(ip_bits)

    @property
    def last_ip(self) -> str:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 1
        ip_bits[-1] = 0

        return ip_conv.bits2strip(ip_bits)

    @property
    def broadcast_ip(self) -> str:
        ip_bits: bitarray = self.ip.bits
        ip_bits[self.mask:] = 1

        return ip_conv.bits2strip(ip_bits)

    @property
    def ips_number(self) -> int:
        pass


if __name__ == "__main__":
    print(sys.argv[1])

    ip_str, mask_str = sys.argv[1].split("/")

    ip: IP = IP(ip_str)

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
