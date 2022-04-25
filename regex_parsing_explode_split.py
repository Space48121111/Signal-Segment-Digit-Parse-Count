from __future__ import annotations
import re
import math
import ast
from typing import Match
from typing import Any

txt = open('regex_parsing_explode_split.txt', 'r')
input1 = txt.read()
input = '''\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''
'''
output = 4140
[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
output1 = 3993
largest magnitude of any two lines, not commutative x + y != y + x
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]] + [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]

addition: include sum = line 1 + line 2
reducing each step:
    explode higher precedence: pair nested in 4 len('[') -> leftmost explodes
        left += [i - 1] and -> disppear to 0 right += [i + 1]
        split: >= 10 leftmost/2 [round down, up]
magnitude: 3 * left + 2 * right recursive next layer

algorithm/brutal force:
regex: compile pair_re left_num_re num_re gt_re
add: {s1}{s2}
reduce: pair >= 4 left_cb: match[0] + pair[1] start= sub(left_cb, s[:pair.start()])
{start}{end} ret s
comp: mag isinstance int or = 3 * v[0] + 2 * v[1]
parse: splitline res = (res, rest) ret comp_sum(res)
double for loop

'''

pair_re = re.compile(r'\[(\d+),(\d+)\]')
left_num_re = re.compile(r'\d+(?!.*\d)')
num_re = re.compile(r'\d+')
gt_re = re.compile(r'\d\d+')

def add_num(s1: str, s2: str) -> str:
    return f'[{s1},{s2}]' # [] count []
def reduce_num(s: str) -> str:
    while True:
        continue_outer = False
        for pair in pair_re.finditer(s):
            # print('Pair ', pair) # <re.Match object; span=(352, 357), match='[4,4]'>
            before = s[:pair.start()]
            # print('Before ', before)
            if before.count('[') - before.count(']') >= 4:
                def left_cb(match: Match(str)) -> str:
                    return str(int(match[0]) + int(pair[1]))
                def right_cb(match: Match(str)) -> str:
                    return str(int(match[0]) + int(pair[2]))
                start = left_num_re.sub(left_cb, s[:pair.start()], count = 1)
                end = num_re.sub(right_cb, s[pair.end():], count = 1)
                s = f'{start}0{end}'
                continue_outer = True
                break
        if continue_outer:
            continue
        gt_num_match = gt_re.search(s)
        if gt_num_match:
            def gt_match_cb(match: Match(str)) -> str:
                val = int(match[0])
                return f'[{math.floor(val / 2)},{math.ceil(val / 2)}]'
            s = gt_re.sub(gt_match_cb, s, count = 1)
            continue
        # print('S ', s)
        return s
def comp_sum(s: str) -> int:
    def comp_val(v: int | Any) -> int:
        if isinstance(v, int):
            return v
        else:
            assert len(v) == 2
            return 3 * comp_val(v[0]) + 2 * comp_val(v[1])
    return comp_val(ast.literal_eval(s))
def parse(s: str) -> int:
    lines = s.splitlines()
    lines = [reduce_num(line) for line in lines]
    res = lines[0]
    for rest in lines[1:]:
        res = reduce_num(add_num(res, rest))
    res = reduce_num(res)
    print('Res ', res)
    return comp_sum(res)

def largest_mag(s: str) -> int:
    lines = s.splitlines()
    largest = 0
    for i, line in enumerate(lines):
        for rest in lines[i + 1:]:
            largest = max(
            largest,
            comp_sum(reduce_num(add_num(line, rest)))
            )
            largest = max(
            largest,
            comp_sum(reduce_num(add_num(rest, line)))
            )
    return largest


# print(parse(input))
print(largest_mag(input1))











# end
