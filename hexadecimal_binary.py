from __future__ import annotations
from typing import NamedTuple
from operator import add, mul, gt, lt, eq

input = '''\
8A004A801A8002F478
'''

'''
110100101111111000101000
VVVTTTAAAAABBBBBCCCCC
output = 2021 in decimal 6 4 0111 1110 0101

00111000000000000110111101000101001010010001001000000000
VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
output = 1 6 0-15-bit 27 10 20

11101110000000001101010000001100100000100011000001100000
VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
output = 7 3 1-11-bit 3 1 2 3

8A004A801A8002F478 16 = op4 op1 op5 lv6
620080001611562C8802118E34 12 = op3-2op(lv) sub
C0015000016115A2E0802F182340 23 =
A0016C880162017C3686B18A3D4780 31 = op1 -op1 -op1 -lv5

hexadecimal -> binary
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111

packet - sub-packets - ignore the trailing 0s
header:
    first 3 bits -> version
    next 3 bits -> type ID nums MSB ignore leading 0s
literal val:
    type id 4  +leading 0s groups of 4 mutiples to divide prefixed by 1 last group prefixed by 0
operator: not type id 4 - operate on sub-packets length mod
    0 -15 bit length in bits of the sub-packets
    1-11 bit nums of the sub-packets
part 1:
parse the hierarchy add up all the version nums
part 2:
type0 sum type1 product type2 min type3 max type5 greater than type6 less type7 equal
C200B40A82 3 = 1 + 2
04005AC33890 54 = 6 + 9
880086C3E88112 7 = min(7, 8, 9)
CE00C43D881120 9 = max
D8005AC2A8F0 1 = 5 < 15
F600BC2D8F 0 = 5 !> 15
9C005AC2F8F0 0 = 5 != 15
9C0141080250320F1802104A08 1 = 1 + 3 = 2 * 2
'''
def parse(line):
    bits = ((int(c, 16) >> i) & 1 for c in line for i in range(3, -1, -1))
    ops = add, mul, lambda *x: max(x), lambda *x: min(x), None, gt, lt, eq
    pos = ver = 0
    def read(size):
        nonlocal pos
        pos += size
        return sum(next(bits) << i for i in range(size - 1, -1, -1))
    def packet():
        nonlocal ver
        ver += read(3)
        print('Ver ', ver)
        if (type := read(3)) == 4:
            go, total = read(1), read(4)
            while go:
                go, total = read(1), total << 4 | read(4)
        elif read(1) == 0:
            length = read(15) + pos
            total = packet()
            while pos < length:
                total = ops[type](total, packet())
        else:
            count = read(11)
            total = packet()
            for _ in range(count - 1):
                total = ops[type](total, packet())
        return total
    total = packet()
    print('Total ', total)
    return ver, total

ver, total = parse(input)
print('Ver, total ', ver, total)

class Packet(NamedTuple):
    ver: int
    type: int
    n: int = -1
    packets: tuple[_Packet, ...] = ()
def compute(s: str) -> int:
    bin_str = ''
    for c in s.strip():
        bin_str += f'{int(c, 16):04b}'
        print('Bin str ', bin_str)
    def parsing(i: int) -> tuple[int, _Packet]:
        def _read(n: int) -> int:
            nonlocal i
            print('i ', i)
            res = int(bin_str[i: i + n], 2)
            i += n
            return res
        ver = _read(3)
        type = _read(3)
        if type == 4:
            n = 0
            chunk = _read(5)
            n = chunk & 0b1111
            while chunk & 0b10000:
                chunk = _read(5)
                n <<= 4
                n += chunk & 0b1111
            print('Chunk ', chunk)
            return i, Packet(ver = ver, type = type, n = n)
        else:
            mode = _read(1)
            if mode == 0:
                bits_length = _read(15)
                j = i
                i += bits_length
                packets = []
                if j < i:
                    j, packet = parsing(j)
                    packets.append(packet)
                    print('Packets ', packets)
                return i, Packet(ver = ver, type = type, packets = tuple(packets))
            else:
                sub_packets = _read(11)
                packets = []
                for _ in range(sub_packets):
                    i, packet = parsing(i)
                    packets.append(packet)
                    print('Packets ', packets)
                return i, Packet(ver = ver, type = type, packets = tuple(packets))
    _, packet = parsing(0)
    stack = [packet]
    total = 0
    while stack:
        pkg = stack.pop()
        total += pkg.ver
        stack.extend(pkg.packets)
    return total

print(compute(input))






# end
