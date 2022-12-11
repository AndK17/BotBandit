from random import randint


def determinant(matrix):
    """Функция вычисляющая детерминат переданной матрицы

    Args:
        matrix (list): Матрица детерминант которой необходимо посчитать

    Returns:
        res (int): Значение детерминанта матрицы
    """
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
    """Функция генерирующая задание с ответом - матрицу и ее детерминант

    Args:
        size (int, optional): Размер стороны квадратной матрицы. Defaults to 3.

    Returns:
        a (list): матрица
        answer (int): детерминант этой матрицы
    """
    a = [[0 for i in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            a[i][j] = randint(0, 10)
    
    answer = determinant(a)
    return a, answer

if __name__ == '__main__':
    print(generate_task())