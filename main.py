from classes import Game
from exceptions import *
import pygame as pg

WIDTH = 800
HEIGHT = 600
LINE_COLOR = (100, 25, 150)    
FRAME_COLOR = (150, 25, 150)
SCREEN_COLOR = (200, 200, 200)
LINE_WIDTH = 2

def choose_dificulty(screen):
    text_color = (134, 45, 78)
    button_color = (45, 228, 67)
    
    myfont = pg.font.SysFont('Corbel', 35)
    mess_font = pg.font.SysFont('Corbel', 50)
    
    BUTTON_WIDTH = WIDTH // 5
    BUTTON_HEIGHT = HEIGHT // 6
    OFFSET_Y = HEIGHT * (2 / 3)
    DISTANCE = WIDTH // 10
        
    message = mess_font.render('Choose difficulty:' , True , text_color)
    easy = myfont.render('easy', True , text_color)
    medium = myfont.render('medium', True , text_color)
    hard = myfont.render('hard', True , text_color)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if DISTANCE <= mouse[0] <= DISTANCE + BUTTON_WIDTH and OFFSET_Y <= mouse[1] <= OFFSET_Y + HEIGHT // 6:
                    return (9, 10)
                if DISTANCE * 2 + BUTTON_WIDTH <= mouse[0] <= DISTANCE * 2 + BUTTON_WIDTH * 2 and OFFSET_Y <= mouse[1] <= OFFSET_Y + HEIGHT // 6:
                    return (16, 35)
                if DISTANCE * 3 + BUTTON_WIDTH * 2 <= mouse[0] <= DISTANCE * 3 + BUTTON_WIDTH * 3 and OFFSET_Y <= mouse[1] <= OFFSET_Y + HEIGHT // 6:
                    return (20, 80)
        screen.fill(SCREEN_COLOR)
        mouse = pg.mouse.get_pos()
        screen.blit(message, (WIDTH // 3, HEIGHT // 2))
        pg.draw.rect(screen, button_color, [DISTANCE, OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT])
        pg.draw.rect(screen, button_color, [DISTANCE * 2 + BUTTON_WIDTH, OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT])
        pg.draw.rect(screen, button_color, [DISTANCE * 3 + BUTTON_WIDTH * 2, OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT])
        screen.blit(easy, (DISTANCE, OFFSET_Y))
        screen.blit(medium, (DISTANCE * 2 + BUTTON_WIDTH, OFFSET_Y))
        screen.blit(hard, (DISTANCE * 3 + BUTTON_WIDTH * 2, OFFSET_Y))
        pg.display.update()

def draw_lines(screen, window, cell_size):
    
    cell = window[0] + cell_size
    while cell < window[0] + window[2]:
        pg.draw.line(
            screen,
            LINE_COLOR,
            (cell, window[1]),
            (cell, window[1] + window[3]),
            LINE_WIDTH
        )
        cell += cell_size
    cell = window[1] + cell_size
    while cell < window[1] + window[3]:
        pg.draw.line(
            screen,
            LINE_COLOR,
            (window[0], cell),
            (window[0] + window[2], cell),
            LINE_WIDTH
        )
        cell += cell_size

def draw_figures(screen, FIELD_SIZE, cell_size, SPACE, field, number_font):
    for row in range(FIELD_SIZE):
        for col in range(FIELD_SIZE):
            if field[row][col].is_opened and field[row][col].value > 0:
                text = number_font.render(str(field[row][col].value), True, (0, 0, 0))
                screen.blit(text, (col * cell_size + SPACE, row * cell_size + SPACE))
            elif field[row][col].is_opened and field[row][col].value == -1:
                text = number_font.render('💣', True, (255, 0, 0))
                screen.blit(text, (col * cell_size + SPACE, row * cell_size + SPACE))
            elif field[row][col].has_flag:
                text = number_font.render('🚩', True, (255, 0, 0))
                screen.blit(text, (col * cell_size + SPACE, row * cell_size + SPACE))
            else:
                pg.draw.rect(
                    screen,
                    (200, 200, 200),
                    (col * cell_size, row * cell_size, cell_size, cell_size)
                )

def endgame(message):
    pass

def main():
    pg.init()

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Minesweeper')
    icon = pg.image.load('assets/icon.png')
    pg.display.set_icon(icon)

    running = True
    dificulty = choose_dificulty(screen)
    while running:
        screen.fill(SCREEN_COLOR)
        
        game = Game(dificulty)
        FONT_SIZE = 16
        window_side = WIDTH * 2 / 3
        window_x, window_y = WIDTH * 1 / 6, HEIGHT * 1 / 18
        field_window = [window_x, window_y, window_side, window_side]
        pg.draw.rect(screen, FRAME_COLOR, field_window)
        cell_size = window_side / game.game_field.size
        draw_lines(screen, field_window, cell_size)
        number_font = pg.font.SysFont(None, FONT_SIZE)
        
        #draw_figures(screen, game.game_field.size, cell_size, SPACE, game.game_field.field, number_font)

        # log = input('Enter the coordinates and mode (mode, x, y): ')
        # try:
        #     mode, x, y = map(int, log.split())
        # except Exception:
        #     print('Enter the mode and coordinates in correct format.')
        #     continue
        # else:
        #     if mode not in (0, 1, 2):
        #         print('There are only 3 modes: 0 - open cell, 1 - place flag, 2 - remove flag.')
        #         continue
        #     if not (0 <= x < game.game_field.size and 0 <= y < game.game_field.size):
        #         print(f'Enter the coordinates in range of the field - (0-{game.game_field.size-1}).')
        #         continue
        #     if game.game_field.field[x][y].is_opened:
        #         print('This cell is already opened.')
        #         continue
        # match mode:
        #     case 0:
        #         if game.game_field.field[x][y].has_flag:
        #             print('You can\'t open a cell with a flag on it.')
        #             continue
        #         new_cell = game.open_cell(x, y)
        #         if new_cell == -1:
        #             print('You lose!')
        #             draw_figures(game.game_field.size, cell_size, SPACE, game.game_field.field, number_font)
        #             ans = input('Do you want to play again? (y/n)\n')
        #             if ans == 'y':
        #                 main()
        #             break
        #         elif game.opened_cells == game.game_field.size ** 2 - game.game_field.mines:
        #             print('You win!')
        #             draw_figures(game.game_field.size, cell_size, SPACE, game.game_field.field, number_font)
        #             ans = input('Do you want to play again? (y/n)\n')  
        #             if ans == 'y':
        #                 main()
        #             break
        #     case 1:
        #         if game.game_field.field[x][y].has_flag:
        #             print('You can\'t open a cell with a flag on it.')
        #             continue
        #         if game.flags == 0:
        #             print('You have no flags left.')
        #             continue
        #         game.put_flag(x, y)
        #     case 2:
        #         if not game.game_field.field[x][y].has_flag:
        #             print('There is no flag on this cell.')
        #             continue
        #         game.remove_flag(x, y)
        # draw_figures(game.game_field.size, cell_size, SPACE, game.game_field.field, number_font)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    running = False
                else:
                    mouse = pg.mouse.get_pos()
                    cord_x, cord_y = mouse[0] - window[0], mouse[1] - window[1]
                    cell_x, cell_y = cord_x // cell_size, cord_y // cell_size
                    if 0 <= cell_x < game.game_field.size and 0 <= cell_y < game.game_field.size:
                        if event.button == 1:
                            if game.opened_cells == 0:
                                game.mine_generate(cell_y, cell_x)
                                game.open_cell(cell_y, cell_x)
                            elif game.game_field.field[cell_y][cell_x] == -1:
                                endgame('You lose!')
                            else:
                                
if __name__ == '__main__':

    
    main()