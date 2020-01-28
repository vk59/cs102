from copy import deepcopy
from typing import List, Optional, Tuple

Map = List[List]
Location = Tuple[int, int]
Health = int


class Labirint:

    def __init__(self, filename: str):
        self.filename = filename
        self.start_hp, self.start_loc, self.map = self.read_file()
        self.max_xp = -1
        self.min_moves = len(self.map) * len(self.map[0])

    def run(self):
        self.find_way(self.start_hp, self.start_loc, self.map)
        self.print_res()

    def read_file(self) -> (Health, Location, Map):
        with open(self.filename) as f:
            loc = tuple(int(num) for num in f.readline().split())
            hp = int(f.readline())
            m = [
                line.split() for line in f]
        return hp, loc, m

    @staticmethod
    def get_next_step(loc: Location, m: Map) -> List[Tuple[int, int]]:
        cells = []
        row, col = loc
        neighbours = ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
        for r, c in neighbours:
            if -1 < r < len(m) and -1 < c < len(m):
                if '0' <= m[r][c] <= '9' or m[r][c] == 'A':
                    cells.append((r, c))
        return cells

    def find_way(self, xp: Health, loc: Location,  matrix: Map, moves: int = 0) -> None:
        x, y = loc
        new_map = deepcopy(matrix)
        if new_map[x][y] == 'A':
            if xp > self.max_xp or xp == self.max_xp and moves < self.min_moves:
                self.map = deepcopy(new_map)
                self.max_xp = xp
                self.min_moves = moves
            return None
        if new_map[x][y] != 'H':
            xp -= int(new_map[x][y])
            new_map[x][y] = 'h' + str(xp)
        if xp < 0:
            return None
        moves += 1
        cells = self.get_next_step(loc, new_map)
        if not cells:
            return None
        for cell in cells:
            self.find_way(xp, cell, new_map, moves)

    def print_res(self):
        file_out = open('ans_' + self.filename, 'w')
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                file_out.write('%+5s' % self.map[i][j])
            file_out.write('\n')
        if self.max_xp != -1:
            file_out.write('Шагов: ' + str(self.min_moves) + '\n Осталось hp: ' + str(self.max_xp))
        else:
            file_out.write('Выхода нет')
        file_out.close()


if __name__ == '__main__':
    for i in range(1, 6):
        game = Labirint('lab{}.txt'.format(i))
        game.run()


