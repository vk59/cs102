import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=5):
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = cell_size * self.life.cols
        self.height = cell_size * self.life.rows
        self.screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.grid = self.life.curr_generation

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(
                            self.screen,
                            pygame.Color('white'), 
                            (i*self.cell_size, j*self.cell_size,
                            self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(
                            self.screen,
                            pygame.Color('green'), 
                            (i*self.cell_size, j*self.cell_size,
                            self.cell_size, self.cell_size))

    def change_status(self) -> None:
        x, y = pygame.mouse.get_pos()
        row = x // self.cell_size
        col = y // self.cell_size
        self.grid[row][col] = (self.grid[row][col] + 1) % 2

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of 'Life'")
        self.screen.fill(pygame.Color('white'))
        self.grid = self.life.curr_generation
        running = True
        pause = False
        while (running and self.life.is_changing and
               not self.life.is_max_generations_exceeded):
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_SPACE:
                    pause = not pause
                elif pause and event.type == MOUSEBUTTONDOWN:
                    self.change_status()
            self.draw_grid()
            self.draw_lines()
            if not pause:
                self.life.step()
            self.grid = self.life.curr_generation
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    life = GameOfLife((30, 30), randomize=True, max_generations=10000)
    game = GUI(life, 20, 9)
    game.run()
