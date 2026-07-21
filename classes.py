from random import randint
from settings import Settings as s
import pygame as pg


class Cell:
    def __init__(self, value=0, is_opened=False, has_flag=False):
        self.value = value
        self.is_opened = is_opened
        self.has_flag = has_flag

    def __repr__(self):
        return f'{self.value}'


class Field:
    def __init__(self, size=9, mines=10):
        self.size = size
        self.field = [[Cell() for _ in range(size)] for _ in range(size)]
        self.mines = mines

    # def show(self):
    #     for stroke in self.field:
    #         print(*stroke, sep=' | ')
    #         print('-' * (self.size * 4 - 1))


class Game:
    def __init__(self, dificulty):
        self.dif = dificulty
        self.game_field = Field(*dificulty)
        self.flags = self.game_field.mines
        self.opened_cells = 0
        self.record = 0
        self.running = True
        self.mine_places = set()

    def __mine_neighbours(self, x, y):
        neighbours = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1),
                      (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        for i, j in neighbours:
            if 0 <= i < self.game_field.size and 0 <= j < self.game_field.size and self.game_field.field[i][j].value >= 0:
                self.game_field.field[i][j].value += 1

    def __remove_empty_cells(self, x, y):
        if not self.game_field.field[x][y].has_flag:
            self.opened_cells += 1
            self.game_field.field[x][y].is_opened = True
            self.__draw_cell(x, y)
            if self.game_field.field[x][y].value == 0:
                neighbors = [(x-1, y-1), (x-1, y), (x-1, y+1),
                             (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
                for i, j in neighbors:
                    if (
                        0 <= i < self.game_field.size and
                        0 <= j < self.game_field.size and
                        not self.game_field.field[i][j].is_opened
                    ):
                        self.__remove_empty_cells(i, j)

    def __draw_cell(self, x, y):
        number_font = pg.font.SysFont(s.font_name, int(s.font_size * 9 / self.dif[0]))
        cell_x, cell_y = (
            s.window[0] + x * (s.cell_size + s.line_width),
            s.window[1] + y * (s.cell_size + s.line_width),
        )
        cell_value = ''
        opened_cell_cords = [
            s.window[0] + x * (s.cell_size + s.line_width) + 2,
            s.window[1] + y * (s.cell_size + s.line_width) + 2,
            s.cell_size - 2,
            s.cell_size - 2,
        ]
        if self.game_field.field[x][y].is_opened:
            opened_cell_color = tuple(map(lambda x: x - 25, s.colors['frame']))
            pg.draw.rect(s.screen, opened_cell_color, opened_cell_cords)
            if self.game_field.field[x][y].value > 0:
                cell_value = f'{self.game_field.field[x][y].value}'
            elif self.game_field.field[x][y].value == -1:
                bomb = pg.image.load('assets/bomb.png').convert_alpha()
                mini_bomb = pg.transform.scale(
                    bomb, (s.cell_size, s.cell_size))
                s.screen.blit(mini_bomb, opened_cell_cords[:2])
        elif self.game_field.field[x][y].has_flag:
            flag = pg.image.load('assets/flag.png').convert_alpha()
            mini_flag = pg.transform.scale(flag, (s.cell_size, s.cell_size))
            s.screen.blit(mini_flag, opened_cell_cords[:2])
        text = number_font.render(cell_value, True, s.colors['text'])
        text_rect = text.get_rect(center=(cell_x + s.cell_size // 2, cell_y + s.cell_size // 2))
        s.screen.blit(text, text_rect)

    def draw_field(self):
        for x in range(self.game_field.size):
            for y in range(self.game_field.size):
                if self.game_field.field[x][y].is_opened or self.game_field.field[x][y].has_flag:
                    self.__draw_cell(x, y)

    def mine_generate(self, x, y):
        occupied = {(x, y), (x-1, y-1), (x-1, y), (x-1, y+1),
                    (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)}
        mines = self.game_field.mines
        while mines > 0:
            new_position = (randint(0, self.game_field.size - 1),
                            randint(0, self.game_field.size - 1))
            if new_position not in occupied:
                mines -= 1
                self.game_field.field[new_position[0]
                                      ][new_position[1]].value = -1
                self.__mine_neighbours(*new_position)
                self.mine_places.add(new_position)
                occupied.add(new_position)
        self.open_cell(x, y)

    def open_cell(self, x, y):
        self.__remove_empty_cells(x, y)
        return self.game_field.field[x][y]

    def put_flag(self, x, y):
        self.game_field.field[x][y].has_flag = True
        self.__draw_cell(x, y)
        self.flags -= 1

    def remove_flag(self, x, y):
        self.game_field.field[x][y].has_flag = False
        self.__draw_cell(x, y)
        self.flags += 1

    def reset(self):
        self.game_field = Field(*self.dif)
        self.flags = self.game_field.mines
        self.opened_cells = 0
        self.mine_places.clear()

    def show_mines(self, delay_ms=100, pause_ms=800):
        delay_ms *= (9 / self.dif[0]) ** 2
        for i, j in self.mine_places:
            if not self.game_field.field[i][j].has_flag:
                self.game_field.field[i][j].is_opened = True
                self.draw_field()
                pg.display.update()
                pg.time.delay(int(delay_ms))
                pg.event.pump()
        pg.time.delay(pause_ms)
