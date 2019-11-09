import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        # Copy from previous assignment
        self.grid = []
        if not randomize:
            for i in range(self.rows):
                self.grid.append([])
                for j in range(self.cols):
                    self.grid[i].append(0)
        else:
            for i in range(self.rows):
                self.grid.append([])
                for j in range(self.cols):
                    self.grid[i].append(random.randint(0,1))
        return self.grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        self.Cells = []
        row, col = cell
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if i != row or j != col:
                    self.Cells.append(self.grid[i][j])

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = self.grid
        self.prev_generation = self.grid
        for i in range(self.rows):
            for j in range(self.cols):
                self.get_neighbours((i,j))
                sum = 0
                for k in range(len(self.Cells)):
                    sum += self.Cells[k]
                if sum < 2 or sum > 3:
                    new_grid[i][j] = 0
                elif sum == 3:
                    new_grid[i][j] = 1
        self.grid = new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        sum = 0
        for i in range(self.rows):
            for j in range(self.cols):
                sum += self.grid[i][j]
        if sum > self.max_generations:
            return True
        return False


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not (self.prev_generation == self.grid)

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        thisFile = open(filename)
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(int(thisFile.read(1)))
        thisFile.close()
        

    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        outFile = open(filename, 'w')
        for i in range(self.rows):
            for j in range(self.cols):
                outFile.write(self.grid[i][j])
        outFile.close()