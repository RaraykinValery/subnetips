# На вход подаётся IP с указанием маски подсети по CIDR
# Например: 192.168.5.20/24
# Программа определяет:
# - подсеть
# - первый IP в подсети
# - последний IP в подсети
# - broadcast IP для подсети
# - сколько всего IP адресов в подсети
#
# Дополнительно интересно было бы определить:
# - разбить сеть на подсети с заданным колвом хостов
# - разбить сеть на определённое количество подсетей
#   с максимальным колвом хостов

import sys
from bitarray import bitarray
import ip_conv
from typing import Callable


class IP:
    def __init__(self, ip: str, mask: str = "") -> None:
        self.ip_str: str = ip
        self.mask: str = mask
        self.intoctets: list[int] = ip_conv.str2intoc(ip)
        self.boctets: list[bitarray] = ip_conv.intoc2boc(self.intoctets)
        self.bits: bitarray = ip_conv.boc2bits(self.boctets)

    def __repr__(self) -> str:
        repr: str = self.ip_str
        if self.mask:
            repr += "/" + self.mask

        return repr


class Subnet:
    def __init__(self, ip: IP, mask: str) -> None:
        self.ip: IP = ip
        self.mask: int = int(mask)

    @property
    def subnet_ip(self) -> IP:
        return self.create_ip(self.apply_subnet_ip_mask)

    @property
    def first_ip(self) -> IP:
        return self.create_ip(self.apply_first_ip_mask)

    @property
    def last_ip(self) -> IP:
        return self.create_ip(self.apply_last_ip_mask)

    @property
    def broadcast_ip(self) -> IP:
        return self.create_ip(self.apply_broadcast_ip_mask)

    @property
    def hosts_count(self) -> int:
        return (2 ** (len(self.ip.bits) - self.mask)) - 2

    def create_ip(self, apply_mask: Callable[[bitarray], bitarray]) -> IP:
        ip_bits: bitarray = apply_mask(self.ip.bits)
        created_ip: IP = IP(ip_conv.bits2strip(ip_bits), str(self.mask))

        return created_ip

    def apply_first_ip_mask(self, ip_bits: bitarray):
        ip_bits[self.mask:] = 0
        ip_bits[-1] = 1

        return ip_bits

    def apply_last_ip_mask(self, ip_bits: bitarray):
        ip_bits[self.mask:] = 1
        ip_bits[-1] = 0

        return ip_bits

    def apply_broadcast_ip_mask(self, ip_bits: bitarray):
        ip_bits[self.mask:] = 1

        return ip_bits

    def apply_subnet_ip_mask(self, ip_bits: bitarray):
        ip_bits[self.mask:] = 0

        return ip_bits


if __name__ == "__main__":
    ip_str: str
    mask_str: str

    ip_str, mask_str = sys.argv[1].split("/")

    ip: IP = IP(ip_str, mask_str)

    subnet = Subnet(ip, mask_str)
    print(f"Subnet IP: {subnet.subnet_ip}")
    print(f"First IP: {subnet.first_ip}")
    print(f"Last IP: {subnet.last_ip}")
    print(f"Broadcast IP: {subnet.broadcast_ip}")
    print(f"Hosts in subnet: {subnet.hosts_count}")

    subnet.mask = 11
    print("\nРезультаты с другой маской подсети:")
    print(f"Subnet IP: {subnet.subnet_ip}")
    print(f"First IP: {subnet.first_ip}")
    print(f"Last IP: {subnet.last_ip}")
    print(f"Broadcast IP: {subnet.broadcast_ip}")
    print(f"Hosts in subnet: {subnet.hosts_count}")
