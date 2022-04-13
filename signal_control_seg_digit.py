# time python signal_control_seg_digit.py
# 0.03s user 0.04s system 69% cpu 0.107 total
# 0.03s user 0.02s system 90% cpu 0.053 total

# input = '''
# be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
# edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
# '''
# the occurence of len([1, 7, 4, 8]) after the | delimiter
# sum(count(len()))

# 1 -> 2 segs gc    1
# 7 -> 3 segs cgb    1
# 4 -> 4 segs gcbe    1
# 8 -> 7 segs fdgacbe dgebacf 2

# straightforward brute force algorithm
# time complexity: O(n + c)
# space complexity: O(n)

# parsing: split('|') -> put each str split(' ') into a set
# count(len(seg)) -> letter no. of each set [2segs: 1]
# translate: for each digit 2segs -> 1

def parse_count(txt):

    # data = input
    txt = open('signal_control_seg_digit.txt', 'r')
    data = txt.read()
    # print(type(data))

    # data = data.replace('|\n', '|')
    # lines = data.strip().splitlines()
    lines = data.splitlines()
    # print(lines)
    count = 0
    for line in lines:
        signal, digit = line.split(' | ')
        # print(digit)
        segs = digit.split()
        for seg in segs:
            # print(seg)
            if len(seg) in {2, 3, 4, 7}:
                # total count of all
                count += 1

    return count


print(parse_count(input))

# def signal_seg_digit(str):
#     # parsing
#     output1, output2 = str.strip().split('\n')
#     # print(output1, output2)
#     signal, digits1 = output1.split('| ')
#     signal, digits2 = output2.split('| ')
#     # print(digits1, digits2)
#     each_digit1 = set(s for s in digits1.split(' '))
#     # set: unique different elements, unordered
#     # list: ordered, may have same elements
#     # each_digit1 = [s for s in digits1.split(' ')]
#     each_digit2 = set(s for s in digits2.split(' '))
#     print(each_digit1)
#     print(each_digit2)
#
#     # loop over and count the digits
#     count_arr = []
#     for seg1 in each_digit1:
#         digit_count = 0
#         for i in seg1:
#             # print(i)
#             digit_count += 1
#         # and put all outcomes into one arr
#         count_arr.append(digit_count)
#         # print(seg1, digit_count)
#     # print(count_arr)
#
#     for seg2 in each_digit2:
#         digit_count = 0
#         for i in seg2:
#             # print(i)
#             digit_count += 1
#         # and put all outcomes into one arr
#         count_arr.append(digit_count)
#         print(seg2, digit_count)
#     print(count_arr)
#
#     # assign the count to specific digit
#     num1, num7, num4, num8 = 0, 0, 0, 0
#     for digit_count in count_arr:
#         if digit_count == 2:
#             num1 += 1
#         elif digit_count == 3:
#             num7 += 1
#         elif digit_count == 4:
#             num4 += 1
#         elif digit_count == 7:
#             num8 += 1
#
#     return num1, num7, num4, num8
#
# print('The nums of 1s, 7s, 4s, 8s are ', signal_seg_digit(input))



# end
