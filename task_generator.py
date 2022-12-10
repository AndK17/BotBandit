from random import randint


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    for i in range(len(matrix[0])):
        if matrix[0][i] == 0:
            if sum([j[i] for j in matrix]) == 0:
                return 0
            
    for i in range(len(matrix[0])):
        if matrix[i][0] == 0:
            if sum(matrix[i]) == 0:
                return 0
    
    res = 0    
    for i in range(len(matrix[0])):
        res += (-1)**i * matrix[i][0] * determinant([j[1:] for j in matrix[0:i]] + [j[1:] for j in matrix[i+1:]])
    return res


def generate_task(size=3):
    answer = -1
    while answer < 0:
        a = [[0 for i in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                a[i][j] = randint(0, 10)
        
        answer = determinant(a)
    return a, answer

if __name__ == '__main__':
    generate_task()