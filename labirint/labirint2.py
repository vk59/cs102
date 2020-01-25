from copy import deepcopy
from collections import Counter
from typing import List, Optional, Tuple


class Labirint:

    def __init__(self,
        filename: str):
        self.filename = filename
        f = open(self.filename)
        ''' 
        Формат входного файла:
        1 стр. - координаты человека loc: tuple[x, y]
        2 стр. - количество жизней у человека xp
        далее записана матрица (карта)
        '''
        self.loc = tuple(int(num) for num in f.readline().split())
        self.xp = int(f.readline())
        self.matrix = []
        for line in f:
            self.matrix.append(line.split())
        # all_ways - все пути, (количество шагов)
        self.all_ways = []
        # all_xps - все конечные xp (ищем наибольший)
        self.all_xps = []
        self.min_moves = 100
        self.max_xp = -1
        f.close()



    def get_next_step(self, loc: Tuple[int, int], matrix: list) -> list:
        
        '''
        Parameter:
            loc - текущее местоположение
        возвращает возможные пути движения (там где нолики или значения больше нуля)
        '''
        cells = []
        row, col = loc
        row1 = row - 1
        if row1 >= 0 and row1 < len(self.matrix):
            place = matrix[row1][col]
            if place >= '0' and place <= '9' or place == 'A':
                    cells.append((row1, col))

        row2 = row + 1
        if row2 >= 0 and row2 < len(self.matrix):
            place = matrix[row2][col]
            if place >= '0' and place <= '9' or place == 'A':
                    cells.append((row2, col))

        col1 = col - 1
        if col1 >= 0 and col1 < len(self.matrix[0]):
            place = matrix[row][col1]
            if place >= '0' and place <= '9' or place == 'A':
                    cells.append((row, col1))

        col2 = col + 1
        if col2 >= 0 and col2 < len(self.matrix[0]):
            place = matrix[row][col2]
            print(place)
            if place >= '0' and place <= '9' or place == 'A':
                    cells.append((row, col2))

        return cells
        

    def find_way(self, xp:int, loc: Tuple[int, int], moves: int, matrix:list) -> None:
        # x, y - текущие координаты
        x, y = loc
        # делаем копию матрицы и рассматриваем новую
        new_matrix = deepcopy(matrix)
        # проверяем, нашли ли мы избушку А
        if new_matrix[x][y] == 'A':
            # если мы нашли какой-то путь, то надо его записать
            self.all_ways.append(moves)
            self.all_xps.append(xp)
            # ищем самый оптимальный путь из тех, что у нас есть
            # 1) минимальные потери 2) минимальная длина
            if max(self.all_xps) == xp and Counter(self.all_xps)[xp] == 1:
                self.matrix = deepcopy(new_matrix)
                self.max_xp = xp
                self.min_moves = moves
            elif Counter(self.all_xps)[xp] > 1 and xp == max(self.all_xps) and moves == min(self.all_ways):
                self.matrix = deepcopy(new_matrix)
                self.max_xp = xp
                self.min_moves = moves
            return None
        # мы не нашли путь. Тогда текущую клетку обозначим h + xp
        if new_matrix[x][y] != 'H':
            xp -= int(new_matrix[x][y])
            new_matrix[x][y] = 'h' + str(xp)
        print(new_matrix)
        # если у нас закончилось xp, то уходим отсюда
        if xp < 0:
            return None
        #  делаем следующий шаг (1 шаг = 10)
        moves += 1
        cells = self.get_next_step(loc, new_matrix)
        print(cells)
        if cells == []:
            return None
        for cell in cells:
            self.find_way(xp, cell, moves, new_matrix)


    def print_res(self):
        fout = open('ans_' + self.filename, 'w')
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                fout.write('%+5s' % self.matrix[i][j])
            fout.write('\n')
        if self.max_xp != -1:
            fout.write('Шагов: ' + str(self.min_moves) + '\n Осталось xp: ' + str(self.max_xp))
        else:
            fout.write('Выхода нет')
        fout.close()


if __name__ == '__main__':
    game = Labirint('lab1.txt')
    game.find_way(game.xp, game.loc, 0, game.matrix)
    game.print_res()
    game = Labirint('lab2.txt')
    game.find_way(game.xp, game.loc, 0, game.matrix)
    game.print_res()
    game = Labirint('lab3.txt')
    game.find_way(game.xp, game.loc, 0, game.matrix)
    game.print_res()
    game = Labirint('lab4.txt')
    game.find_way(game.xp, game.loc, 0, game.matrix)
    game.print_res()
    game = Labirint('lab5.txt')
    game.find_way(game.xp, game.loc, 0, game.matrix)
    game.print_res()




"""
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


    def find_way(self, loc: Tuple[int, int], moves: int):
        x, y = self.loc
        new_matrix = deepcopy(self.matrix)
        if new_matrix[x][y] == 'A':
            self.all_ways.append(moves)
            return None
        if self.matrix[x][y] != 'H':
            self.matrix[x][y] = 'x'
        print(self.loc)
        print(self.matrix)
        moves += 10
        cells = self.get_next_step(self.loc)
        if cells == []:
            pass
        for cell in cells:
            self.loc = cell
            self.find_way(self.loc, moves)
"""