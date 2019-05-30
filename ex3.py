import numpy as np
import sys
blank = '_'

matrix_file = "mat.npy" if len(sys.argv) <4 else sys.argv[2]
mat = np.load(matrix_file).T
expected_output = "ab" if len(sys.argv) <4 else sys.argv[2]
vocabulary = "ab" if len(sys.argv) <4 else sys.argv[3]

vocabulary += blank
probability = {}
for row_number,cha in enumerate(vocabulary):
        probability[cha] = mat[row_number]

expected_with_blanks = blank + blank.join(expected_output) + blank
# print(expected_with_blanks)


time_slots = len(mat[0])
cal_matrix = np.zeros((len(expected_with_blanks), time_slots))
cal_matrix[0,0] = probability[expected_with_blanks[0]][0]
cal_matrix[1,0] = probability[expected_with_blanks[1]][0]
# print(cal_matrix)


def get_val(matrix, row, col):
    if row<0 or col < 0:
        return 0
    if row > len(matrix) or col > len(matrix[0]):
        return 0
    return matrix[row,col]



for t in range(1, time_slots):
    for char_index in range(len(expected_with_blanks)):

        if expected_with_blanks[char_index] == blank or (char_index > 1 and expected_with_blanks[char_index] == expected_with_blanks[char_index - 2]):
            cal_matrix[char_index,t] = (get_val(cal_matrix,char_index-1,t-1) + get_val(cal_matrix,char_index,t-1)) * probability[expected_with_blanks[char_index]][t]
        else:
            cal_matrix[char_index, t] = ( get_val(cal_matrix,char_index-2,t-1) + get_val(cal_matrix,char_index-1,t-1) + get_val(cal_matrix,char_index,t-1) ) *  probability[expected_with_blanks[char_index]][t]

result = cal_matrix[-1,-1] + cal_matrix[-2,-1]
print(result)
