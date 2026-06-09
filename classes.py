from random import randint


class Cell:
    def __init__(self, value=0, is_opened=False, has_flag=False):
        self.value = value
        self.is_opened = is_opened
        self.has_flag = has_flag

    def __repr__(self):
        if not self.is_opened:
            return ' ' if not self.has_flag else '|>'
        else:
            return f'{self.value}'


class Field:
    def __init__(self, size=9, mines=10):
        self.size = size
        self.field = [[Cell() for _ in range(size)] for _ in range(size)]
        self.mines = mines

    def show(self):
        for stroke in self.field:
            print(*stroke, sep=' | ')
            print('-' * (self.size * 4 - 1))


class Game:
    def __init__(self, dificulty):
        self.game_field = Field(*dificulty)
        self.flags = self.game_field.mines
        self.opened_cells = 0

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

    def mine_generate(self, x, y):
        occupied = {(x, y), (x-1, y-1), (x-1, y), (x-1, y+1),
                    (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)}
        mines = self.game_field.mines
        while mines > 0:
            new_position = (randint(0, self.game_field.size - 1),
                            randint(0, self.game_field.size - 1))
            if new_position not in occupied:
                mines -= 1
                self.game_field.field[new_position[0]][new_position[1]].value = -1
                self.__mine_neighbours(*new_position)
                occupied.add(new_position)
        self.open_cell(x, y)

    def open_cell(self, x, y):
        self.__remove_empty_cells(x, y)
        return self.game_field.field[x][y].value

    def put_flag(self, x, y):
        self.game_field.field[x][y].has_flag = True
        self.flags -= 1

    def remove_flag(self, x, y):
        self.game_field.field[x][y].has_flag = False
        self.flags += 1
