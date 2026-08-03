from random import randint
from settings import Settings as s
from settings import SFX as sfx
from settings import PlayWindow as p
from settings import IMG as img
import pygame as pg
import csv

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
        self.best_record = self.get_best_result()
        self.running = True
        self.mine_places = set()
        self.expire_time = None
        
    def __mine_neighbours(self, x, y):
        neighbours = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1),
                      (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        for i, j in neighbours:
            if 0 <= i < self.game_field.size and 0 <= j < self.game_field.size and self.game_field.field[i][j].value >= 0:
                self.game_field.field[i][j].value += 1

    def __remove_empty_cells(self, x, y, delay_ms=10):
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
                        pg.time.delay(delay_ms)
                        pg.display.update()
                        self.__remove_empty_cells(i, j)

    def __draw_cell(self, x, y):
        number_font = pg.font.SysFont(s.font_name, int(s.font_size * 9 / self.dif[0]))
        cell_x, cell_y = (
            p.window[0] + x * (p.cell_size + s.line_width),
            p.window[1] + y * (p.cell_size + s.line_width),
        )
        cell_value = ''
        opened_cell_cords = [
            p.window[0] + x * (p.cell_size + s.line_width) + s.line_width,
            p.window[1] + y * (p.cell_size + s.line_width) + s.line_width,
            p.cell_size - s.line_width // 2,
            p.cell_size - s.line_width // 2,
        ]
        if self.game_field.field[x][y].is_opened:
            opened_cell_color = tuple(map(lambda x: x - 25, s.colors['frame']))
            pg.draw.rect(s.screen, opened_cell_color, opened_cell_cords)
            if self.game_field.field[x][y].value > 0:
                cell_value = f'{self.game_field.field[x][y].value}'
            elif self.game_field.field[x][y].value == -1:
                bomb = pg.transform.scale(
                    img.picture('bomb'), (p.cell_size, p.cell_size))
                s.screen.blit(bomb, opened_cell_cords[:2])
        elif self.game_field.field[x][y].has_flag:
            flag = pg.transform.scale(img.picture('flag'), (int(p.cell_size * 0.95), p.cell_size))
            s.screen.blit(flag, opened_cell_cords[:2])
        else:
            pg.draw.rect(s.screen, s.colors['frame'], opened_cell_cords)
        text = number_font.render(cell_value, True, s.colors['text'])
        text_rect = text.get_rect(center=(cell_x + p.cell_size // 2, cell_y + p.cell_size // 2))
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
        sfx.all_sounds['flag'].play()

    def remove_flag(self, x, y):
        self.game_field.field[x][y].has_flag = False
        self.__draw_cell(x, y)
        self.flags += 1
        sfx.all_sounds['reset_flag'].play()

    def reset(self):
        self.game_field = Field(*self.dif)
        self.flags = self.game_field.mines
        self.opened_cells = 0
        self.mine_places.clear()
        self.is_new = True
        self.best_record = self.get_best_result()
        if s.cruel_mode:
            from time import time
            self.expire_time = time() + s.time_params[s.current_difficulty]
            
    def show_mines(self, delay_ms=100, pause_ms=800):
        if not self.mine_places:
            s.screen.blit(pg.transform.scale(img.picture('bomb'), p.window[2:]), p.window[:2])
            sfx.all_sounds['bomb'].play()
            pg.display.update()
        for i, j in self.mine_places:
            if not self.game_field.field[i][j].has_flag:
                self.game_field.field[i][j].is_opened = True
                self.__draw_cell(i, j)
                sfx.all_sounds['bomb'].play()
                pg.display.update()
                pg.time.delay(delay_ms)
                pg.event.pump()
        pg.time.delay(pause_ms)

        
    def get_best_result(self):
        results_file = 'best_results.csv' if not s.cruel_mode else 'best_results_cruel.csv'
        try:
            with open(results_file, 'r+', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['difficulty'] == s.current_difficulty:
                        return int(row['record'])
                writer = csv.DictWriter(file, fieldnames=['difficulty', 'record'])
                writer.writerow({'difficulty': s.current_difficulty, 'record': 0})
                return 0
        except FileNotFoundError:
            with open(results_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['difficulty', 'record'])
                writer.writeheader()
                writer.writerow({'difficulty': s.current_difficulty, 'record': 0})
                return 0
                
    def change_result(self):
        rows = []
        results_file = 'best_results.csv' if not s.cruel_mode else 'best_results_cruel.csv'
        with open(results_file, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['difficulty'] == s.current_difficulty:
                    rows.append({'difficulty': s.current_difficulty, 'record': self.record})
                    continue
                rows.append(row)
        with open(results_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['difficulty', 'record'])
            writer.writeheader()
            writer.writerows(rows)