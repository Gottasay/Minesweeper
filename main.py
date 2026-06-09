from classes import Game
from exceptions import *
import pygame as pg

def choose_dificulty():
    while True:
        DIFICULTIES = {
            'easy': (9, 10),
            'medium': (16, 35),
            'hard': (20, 80)
                        }
        curr_dif = input('Choose the dificulty: easy, medium, hard\n')
        match curr_dif:
            case 'easy':
                dif = DIFICULTIES['easy']
                return dif
            case 'medium':
                dif = DIFICULTIES['medium']
                return dif
            case 'hard':
                dif = DIFICULTIES['hard']
                return dif
            case _:
                print('Incorrect input. Try again')
         
def main():
    dificulty = choose_dificulty()
    game = Game(dificulty)
    game.game_field.show()
    while True:
        try:
            x, y = map(int, input('Enter the coordinates (x y): ').split())
            game.mine_generate(x, y)
        except Exception:
            print('Enter only integer coordinates.')
        else:
            break
        
    game.game_field.show()
    
    while True:
        log = input('Enter the coordinates and mode (mode, x, y): ')
        try:
            mode, x, y = map(int, log.split())
        except Exception:
            print('Enter the mode and coordinates in correct format.')
            continue
        else:
            if mode not in (0, 1, 2):
                print('There are only 3 modes: 0 - open cell, 1 - place flag, 2 - remove flag.')
                continue
            if not (0 <= x < game.game_field.size and 0 <= y < game.game_field.size):
                print(f'Enter the coordinates in range of the field - (0-{game.game_field.size-1}).')
                continue
            if game.game_field.field[x][y].is_opened:
                print('This cell is already opened.')
                continue
        match mode:
            case 0:
                if game.game_field.field[x][y].has_flag:
                    print('You can\'t open a cell with a flag on it.')
                    continue
                new_cell = game.open_cell(x, y)
                if new_cell == -1:
                    print('You lose!')
                    game.game_field.show()
                    ans = input('Do you want to play again? (y/n)\n')
                    if ans == 'y':
                        main()
                    break
                elif game.opened_cells == game.game_field.size ** 2 - game.game_field.mines:
                    print('You win!')
                    game.game_field.show()
                    ans = input('Do you want to play again? (y/n)\n')  
                    if ans == 'y':
                        main()
                    break
            case 1:
                if game.game_field.field[x][y].has_flag:
                    print('You can\'t open a cell with a flag on it.')
                    continue
                if game.flags == 0:
                    print('You have no flags left.')
                    continue
                game.put_flag(x, y)
            case 2:
                if not game.game_field.field[x][y].has_flag:
                    print('There is no flag on this cell.')
                    continue
                game.remove_flag(x, y)
        game.game_field.show()

if __name__ == '__main__':
    main()