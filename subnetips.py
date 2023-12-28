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

import sys


class IP:
    def __init__(self, ip: str, mask: str):
        self.ip: list = list(map(lambda x: int(x), ip.split(".")))
        self.mask: int = int(mask)

    def subnet(self):
        self.print_result(self.__get_subnet())

    def __get_subnet(self) -> list:
        immutable_octets_number: int = self.mask // 8
        immutable_bits_number: int = self.mask % 8
        partially_modifiable_octet_index: int = immutable_octets_number

        subnet: list = []

        for i in range(immutable_octets_number):
            subnet.append(self.ip[i])

        bit_mask: str = ('1' * immutable_bits_number
                         + '0' * (8 - immutable_bits_number))
        bit_mask_decimal: int = int(bit_mask, 2)

        subnet.append(
            self.ip[partially_modifiable_octet_index]
            & bit_mask_decimal
        )

        for i in range(4 - (partially_modifiable_octet_index + 1)):
            subnet.append(0)

        return subnet

    def print_result(self, result: list):
        print(f'{".".join(list(map(lambda x: str(x), result)))}/{self.mask}')


class Subnet:
    def __init__(self, ip: str, mask: str):
        self.subnet: list = list(map(lambda x: int(x), ip.split(".")))
        self.mask: int = int(mask)

    def first_ip(self):
        self.print_result(self.__get_first_ip())

    def last_ip(self):
        self.print_result(self.__get_last_ip())

    def broadcast_ip(self):
        self.print_result(self.__get_broadcast_ip())

    def __get_first_ip(self):
        first_ip: list = self.subnet
        first_ip[-1] = first_ip[-1] | 1

        return first_ip

    def __get_last_ip(self):
        immutable_octets_number: int = self.mask // 8
        immutable_bits_number: int = self.mask % 8
        partially_modifiable_octet_index: int = immutable_octets_number

        last_ip: list = []

        for i in range(immutable_octets_number):
            last_ip.append(self.subnet[i])

        bit_mask: str = ('0' * immutable_bits_number
                         + '1' * (8 - immutable_bits_number))
        bit_mask_decimal: int = int(bit_mask, 2)

        last_ip.append(
            self.subnet[partially_modifiable_octet_index]
            | bit_mask_decimal
        )

        for i in range(4 - (partially_modifiable_octet_index + 1)):
            last_ip.append(255)

        last_ip[-1] = last_ip[-1] ^ 1

        return last_ip

    def __get_broadcast_ip(self):
        immutable_octets_number: int = self.mask // 8
        immutable_bits_number: int = self.mask % 8
        partially_modifiable_octet_index: int = immutable_octets_number

        broadcast_ip: list = []

        for i in range(immutable_octets_number):
            broadcast_ip.append(self.subnet[i])

        bit_mask: str = ('0' * immutable_bits_number
                         + '1' * (8 - immutable_bits_number))
        bit_mask_decimal: int = int(bit_mask, 2)

        broadcast_ip.append(
            self.subnet[partially_modifiable_octet_index]
            | bit_mask_decimal
        )

        for i in range(4 - (partially_modifiable_octet_index + 1)):
            broadcast_ip.append(255)

        return broadcast_ip

    def print_result(self, result: list):
        print(f'{".".join(list(map(lambda x: str(x), result)))}/{self.mask}')


if __name__ == "__main__":
    print(sys.argv[1])

    ip = IP(*sys.argv[1].split("/"))
    ip.subnet()
    subnet = Subnet(*"192.168.32.0/20".split("/"))
    subnet.first_ip()
    subnet.last_ip()
    subnet.broadcast_ip()
