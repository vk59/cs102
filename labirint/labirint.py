def find_way(x, y, moves):
    # попытка вправо
    find_way(x, y + 1, )
    
    return -1


for i in range(2):
    # reading data from file
    f = open('lab{}.txt'.format(i + 1))
    ''' 
        Формат входного файла:
        1 стр. - координаты человека a b
        2 стр. - количество жизней у человека L
        далее записана матрица (карта)
    '''
    a, b = tuple(f.readline().split())
    L = int(f.readline())
    matrix = []
    for line in f:
        matrix.append(line.split())
    find_way(a, b, 0)
    f.close()