from __future__ import annotations
from functools import reduce
from typing import Literal
from dataclasses import dataclass, field
from utils import read_lines
from enum import IntEnum


Bit = Literal['0', '1']
Binary = list[Bit]

LITERAL_VALUE_PACKET_TYPE = 4

class PacketType(IntEnum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    VALUE = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


@dataclass
class LiteralValuePacket:
    version: int = 0
    type: PacketType = PacketType.VALUE
    value: int = 0


@dataclass
class OperatorPacket:
    version: int = 0
    type: PacketType = PacketType.SUM
    packets: list[Packet] = field(default_factory=list)


Packet = LiteralValuePacket | OperatorPacket


def get_bin_from_hex(hex: str) -> Binary:
    num = int(hex, base=16)
    num_bin = bin(num)
    num_bin = num_bin[2:]
    if len(num_bin) % 4 != 0:
        correct_length = (len(num_bin) // 4 + 1) * 4
        num_zeros = correct_length - len(num_bin)
        num_bin = '0' * num_zeros + num_bin
    return [bit for bit in num_bin if bit == '1' or bit == '0']


def get_literal_value_packet(packet: Binary) -> tuple[LiteralValuePacket, Binary]:
    version = int(''.join(packet[:3]), base=2)
    packet = packet[6:]
    is_not_finished = True
    value_str = ''
    while is_not_finished:
        sub = packet[:5]
        if sub[0] == '0':
            is_not_finished = False
        sub_value_bin = ''.join(sub[1:])
        value_str += sub_value_bin
        packet = packet[5:]
    value = int(value_str, base=2)
    return LiteralValuePacket(version, PacketType.VALUE, value), packet


def get_packet(packet: Binary) -> tuple[Packet, Binary]:
    type = int(''.join(packet[3:6]), base=2)
    if type == LITERAL_VALUE_PACKET_TYPE:
        return get_literal_value_packet(packet)
    else:
        return get_operator_packet(packet)


def get_operator_packet(packet: Binary) -> tuple[OperatorPacket, Binary]:
    version = int(''.join(packet[:3]), base=2)
    packet = packet[3:]
    type = PacketType(int(''.join(packet[:3]), base=2))
    packet = packet[3:]
    length_id = packet[0]
    packet = packet[1:]
    match length_id:
        case '0':
            length = int(''.join(packet[:15]), base=2)
            packet = packet[15:]
            sub_packets = packet[:length]
            packet = packet[length:]
            other_packets: list[Packet] = []
            while len(sub_packets) != 0:
                other_packet, remaining_sub_packets = get_packet(sub_packets)
                other_packets.append(other_packet)
                sub_packets = remaining_sub_packets
            return OperatorPacket(version=version, type=type, packets=other_packets), packet
        case '1':
            num_sub_packets = int(''.join(packet[:11]), base=2)
            packet = packet[11:]
            other_packets: list[Packet] = []
            for _ in range(num_sub_packets):
                other_packet, remaining_packet = get_packet(packet)
                other_packets.append(other_packet)
                packet = remaining_packet
            return OperatorPacket(version=version, type=type, packets=other_packets), packet


def get_packet_versions_sum(packet: Packet) -> int:
    match packet:
        case LiteralValuePacket(version=version):
            return version
        case OperatorPacket(version=version, packets=other_packets):
            sum = version
            for other_packet in other_packets:
                sum += get_packet_versions_sum(other_packet)
            return sum

def get_packet_value(packet: Packet) -> int:
    match packet:
        case LiteralValuePacket(value=value):
            return value
        case OperatorPacket(type=type, packets=other_packets):
            match type:
                case PacketType.SUM:
                    return sum([get_packet_value(other_packet) for other_packet in other_packets])
                case PacketType.PRODUCT:
                    return reduce(lambda x, y: x * y ,[get_packet_value(other_packet) for other_packet in other_packets])
                case PacketType.MINIMUM:
                    return min([get_packet_value(other_packet) for other_packet in other_packets])
                case PacketType.MAXIMUM:
                    return max([get_packet_value(other_packet) for other_packet in other_packets])
                case PacketType.GREATER_THAN:
                    first = get_packet_value(other_packets[0])
                    second = get_packet_value(other_packets[1])
                    return 1 if first > second else 0
                case PacketType.LESS_THAN:
                    first = get_packet_value(other_packets[0])
                    second = get_packet_value(other_packets[1])
                    return 1 if first < second else 0
                case PacketType.EQUAL_TO:
                    first = get_packet_value(other_packets[0])
                    second = get_packet_value(other_packets[1])
                    return 1 if first == second else 0
                case _:
                    return 0

def get_packet_bin(path: str) -> Binary:
    line = read_lines(path)[0]
    return get_bin_from_hex(line)


def solve_part_one() -> None:
    packet_binary = get_packet_bin('day_sixteen.txt')
    packet, _ = get_packet(packet_binary)
    sum = get_packet_versions_sum(packet)
    print(sum)


def solve_part_two() -> None:
    packet_binary = get_packet_bin('day_sixteen.txt')
    packet, _ = get_packet(packet_binary)
    value = get_packet_value(packet)
    print(value)


if __name__ == '__main__':
    solve_part_two()