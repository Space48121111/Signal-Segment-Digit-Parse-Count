from __future__ import annotations
from collections import Counter
import itertools
import functools

txt = open('dice_game.txt', 'r')
input1 = txt.read()
input = '''\
Player 1 starting position: 4
Player 2 starting position: 8
'''

'''
output = 739785 = 745 * 993 score(losing player) * no(die rolled)
output1 = 444356092776315, 341960390180808 3 universes scores >= 21
quantum die each roll 3 copies/outcomes
deterministic 100 sided die roll 3 times every turn for each player 1-10
while n > 10:
    n -= 10
parsing: splitlines lines[0].split()
for i in range(1, 101)
    i, i + 1, i + 2
    i + 3, i + 4, i + 5
        score += n(sum(score))
        rolls += 3
if score > 1000 break
return min(score1, score2), rolls
'''
def weird_mod(n: int) -> int:
    while n > 10:
        n -= 10
    return n

def compute(s: str) -> int:
    lines = s.splitlines()
    _, _, _, _, p1_s = lines[0].split()
    _, _, _, _, p2_s = lines[1].split()
    p1, p2 = int(p1_s), int(p2_s)

    rolls = 0
    die = itertools.cycle(range(1, 101))
    score1 = score2 = 0
    while True:
        print('P1 ', p1)
        p1 = weird_mod(p1 + next(die) + next(die) + next(die))
        rolls += 3
        score1 += p1
        print('Score1 ', score1)
        if score1 >= 1000:
            break
        print('P2 ', p2)
        p2 = weird_mod(p2 + next(die) + next(die) + next(die))
        rolls += 3
        score2 += p2
        print('Score2 ', score2)
        if score2 >= 1000:
            break
    print(rolls, score1, score2)
    return rolls * min(score1, score2)

def compute1(s: str) -> int:
    lines = s.splitlines()
    _, _, _, _, p1_s = lines[0].split()
    _, _, _, _, p2_s = lines[1].split()
    p_1, p_2 = int(p1_s), int(p2_s)
    # 27 = 3 * 3 * 3 universes overlaps
    die = Counter(i + j + k for i in (1, 2, 3) \
    for j in (1, 2, 3) for k in (1, 2, 3))
    # Functions that act on or return other functions
    # LRU least recently used
    @functools.lru_cache(maxsize = None)
    def comp_win_ct(p1: int, s1: int, p2: int, s2: int) -> tuple[int, int]:
        p1_w = p2_w = 0
        for i, ct in die.items():
            # print('Initial p1 s1 ', p1, s1)
            n_p1 = weird_mod(p1 + i)
            n_s1 = s1 + n_p1
            # print('New p1 s1', n_p1, n_s1)
            if n_s1 >= 21:
                p1_w += ct
                # print('P1 w ', p1_w)
            else:
                tmp_p2_w, tmp_p1_w = comp_win_ct(p2, s2, n_p1, n_s1)
                # print('Second p1 w p2 w', tmp_p1_w, tmp_p2_w)
                p1_w += tmp_p1_w * ct
                p2_w += tmp_p2_w * ct
        # print('In loop p1 w p2 w ', p1_w, p2_w)
        return p1_w, p2_w
    p1_w_b, p2_w_b = comp_win_ct(p_1, 0, p_2, 0)
    print('End p1 w p2 w ', p1_w_b, p2_w_b)
    return max(p1_w_b, p2_w_b)

'''
Initial p1 s1  4 0
New p1 s1 7 7
P1 w  1
Initial p1 s1  4 0
New p1 s1 8 8
P1 w  4
Initial p1 s1  4 0
New p1 s1 9 9
P1 w  10
Initial p1 s1  4 0
New p1 s1 10 10
P1 w  17
Initial p1 s1  4 0
New p1 s1 1 1
Initial p1 s1  8 0
New p1 s1 1 1
Initial p1 s1  1 1
New p1 s1 4 5
P1 w  1
Initial p1 s1  1 1
New p1 s1 5 6
P1 w  4
Initial p1 s1  1 1
New p1 s1 6 7
P1 w  10
Initial p1 s1  1 1
New p1 s1 7 8
P1 w  17
Initial p1 s1  1 1
New p1 s1 8 9
P1 w  23
Initial p1 s1  1 1
New p1 s1 9 10
P1 w  26
Initial p1 s1  1 1
New p1 s1 10 11
P1 w  27
In loop p1 w p2 w  27 0
Second p1 w p2 w 0 27
Initial p1 s1  8 0
New p1 s1 2 2
Initial p1 s1  1 1
New p1 s1 4 5
P1 w  1
Initial p1 s1  1 1
New p1 s1 5 6
P1 w  4
...
Initial p1 s1  8 0
New p1 s1 6 6
P1 w  22
Initial p1 s1  8 0
New p1 s1 7 7
P1 w  23
In loop p1 w p2 w  23 108
Second p1 w p2 w 108 23
Initial p1 s1  4 0
New p1 s1 3 3
P1 w  990
In loop p1 w p2 w  990 207
End p1 w p2 w  990 207
'''

# print(compute(input))
print(compute1(input))












# end
