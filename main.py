from classes import Game, Field
from exceptions import *
from settings import Settings as s
import pygame as pg

WIDTH = s.width
HEIGHT = s.height
LINE_COLOR = s.colors['line']
FRAME_COLOR = s.colors['frame']
SCREEN_COLOR = s.colors['screen']
LINE_WIDTH = s.line_width

            
def choose_dificulty():
    button_color = tuple(map(lambda x: x - 50, s.colors['screen']))
    but_size, mess_size = 35, 50
    but_font = pg.font.SysFont(s.font_name, but_size)
    mess_font = pg.font.SysFont(s.font_name, mess_size)
    
    BUTTON_WIDTH = WIDTH // 5
    BUTTON_HEIGHT = HEIGHT // 6
    OFFSET_Y = int(HEIGHT * (2 / 3))
    DISTANCE = WIDTH // 10
    choose_msg = 'Choose difficulty:'
    message = mess_font.render(choose_msg, True , s.colors['text'])
    difs = ['easy', 'medium', 'hard']
    
    while True:
        s.screen.fill(SCREEN_COLOR)
        mouse = pg.mouse.get_pos()
        s.screen.blit(message, ((s.width - len(choose_msg) * mess_size // 2) // 2, HEIGHT // 3))
        dist = DISTANCE
        for dif in difs:
            pg.draw.rect(s.screen, button_color, (dist, OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
            pg.draw.rect(s.screen, tuple(map(lambda x: x - 50, button_color)), (dist, OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT), width=2, border_radius=10)
            cur_dif = but_font.render(dif, True, s.colors['text'])
            dif_cord = (dist + (BUTTON_WIDTH - cur_dif.get_width()) // 2, OFFSET_Y + (BUTTON_HEIGHT - cur_dif.get_height()) // 2)
            s.screen.blit(cur_dif, dif_cord)
            dist += DISTANCE + BUTTON_WIDTH
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if DISTANCE <= mouse[0] <= DISTANCE + BUTTON_WIDTH and OFFSET_Y <= mouse[1] <= OFFSET_Y + HEIGHT // 6:
                    return (9, 10)
                if DISTANCE * 2 + BUTTON_WIDTH <= mouse[0] <= DISTANCE * 2 + BUTTON_WIDTH * 2 and OFFSET_Y <= mouse[1] <= OFFSET_Y + HEIGHT // 6:
                    return (16, 35)
                if DISTANCE * 3 + BUTTON_WIDTH * 2 <= mouse[0] <= DISTANCE * 3 + BUTTON_WIDTH * 3 and OFFSET_Y <= mouse[1] <= OFFSET_Y + HEIGHT // 6:
                    return (20, 80)
        
        pg.display.update()

def main_menu():
    msg = 'Welcome to Minesweeper!'
    play_msg = 'Start'
    
    msg_size, play_size = 50, 40
    msg_font = pg.font.SysFont(s.font_name, msg_size)
    play_font = pg.font.SysFont(s.font_name, play_size)
    
    msg_cords = (s.width - len(msg) * msg_size // 2) // 2, s.height // 12
    play_button_cords = [s.width // 4, s.height * 3 // 4, s.width // 2, s.height // 10]
    play_msg_cords = [(s.width - len(play_msg) * play_size // 2) // 2, play_button_cords[1]]
    picture_cords = [s.width // 4, s.height // 5, s.width // 2, s.height // 2]
    
    picture = pg.image.load('assets/main.jpg').convert_alpha()
    mini_picture = pg.transform.scale(picture, picture_cords[2:])
    play_button_color = tuple(map(lambda x: x - 25, s.colors['screen']))
    while True:
        s.screen.fill(SCREEN_COLOR)
        mouse = pg.mouse.get_pos()
        s.screen.blit(msg_font.render(msg, True, s.colors['text']), msg_cords)
        pg.draw.rect(s.screen, play_button_color, play_button_cords)
        pg.draw.rect(s.screen, tuple(map(lambda x: x - 30, play_button_color)), play_button_cords, width=3)
        s.screen.blit(play_font.render(play_msg, True, s.colors['text']), play_msg_cords)
        s.screen.blit(mini_picture, picture_cords[:2])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if (play_button_cords[0] <= mouse[0] <= play_button_cords[0] + play_button_cords[2] and
                play_button_cords[1] <= mouse[1] <= play_button_cords[1] + play_button_cords[3]):
                    return choose_dificulty()
        pg.display.update()    
                    
def draw_lines(screen, size, cell_size):
    left, top = s.window[0], s.window[1]
    width, height = s.window[2], s.window[3]

    for i in range(0, size + 1):
        x = left + i * (cell_size + s.line_width)
        y = top + i * (cell_size + s.line_width)
        pg.draw.line(screen, LINE_COLOR, (x, top), (x, top + height), LINE_WIDTH)
        pg.draw.line(screen, LINE_COLOR, (left, y), (left + width, y), LINE_WIDTH)


def stop_game(game, type=0):
    end = {0: {'message': 'You lose!'}, 1: {'message': 'You win!'}, 2: {'message': 'Game paused!'}}
    mess_font = pg.font.SysFont(s.font_name, s.font_size)
    msg = mess_font.render(end[type]['message'], True, s.colors['text'])
    record = f'Your record: {game.record}'
    record_msg = mess_font.render(record, True, s.colors['text'])
    while True:
        x, y, a, b = s.width // 4, s.height // 4, s.width // 2, s.height // 1.8
        rect_cords = [x, y, a, b]
        button_1_cords = [x + a // 10, y + int(b * 23/30), a // 5, b // 5]
        button_2_cords = [x + int(a * 7/10), button_1_cords[1], a // 5, b // 5]
        rect_color = s.colors['screen']
        button_color = tuple(map(lambda x: x - 30, s.colors['screen']))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                game.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    game.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse = event.pos
                if button_1_cords[0] <= mouse[0] <= button_1_cords[0] + button_1_cords[2] and button_1_cords[1] <= mouse[1] <= button_1_cords[1] + button_1_cords[3]:
                    main()
                elif button_2_cords[0] <= mouse[0] <= button_2_cords[0] + button_2_cords[2] and button_2_cords[1] <= mouse[1] <= button_2_cords[1] + button_2_cords[3]:
                    game.reset()
                    return
        pg.draw.rect(s.screen, rect_color, rect_cords)
        pg.draw.rect(s.screen, button_color, rect_cords, width=5)
        pg.draw.rect(s.screen, button_color, button_1_cords)
        pg.draw.rect(s.screen, button_color, button_2_cords)
        pg.draw.rect(s.screen, tuple(map(lambda x: x - 30, button_color)), button_1_cords, width=3)
        pg.draw.rect(s.screen, tuple(map(lambda x: x - 30, button_color)), button_2_cords, width=3)
        home = pg.image.load('assets/home.png').convert_alpha()
        mini_home = pg.transform.scale(home, button_1_cords[2:])
        s.screen.blit(mini_home, button_1_cords[:2])
        if type == 0:
            game.record = 0
            arrow = 'assets/retry.png'
            picture = 'assets/cat.png'
            pic = pg.image.load(picture).convert_alpha()
            mini_pic = pg.transform.scale(pic, (a // 2, b // 2))
            s.screen.blit(mini_pic, (x + a // 4, y + b // 4))      
        elif type == 1:
            arrow = 'assets/next.png'
            picture = 'assets/simpson.jpg'
            pic = pg.image.load(picture).convert_alpha()
            mini_pic = pg.transform.scale(pic, (a // 2, b // 2))
            s.screen.blit(mini_pic, (x + a // 4, y + b // 4))
        else:
            arrow = 'assets/retry.png'
        sign = pg.image.load(arrow).convert_alpha()
        mini_sign = pg.transform.scale(sign, button_2_cords[2:])
        s.screen.blit(mini_sign, button_2_cords[:2])
        # Центрируем сообщения внутри окна rect_cords = [x, y, a, b]
        center_x = x + a // 2
        center_y = y + b // 2
        # Сместим основное сообщение чуть выше центра, а рекорд чуть ниже
        msg_rect = msg.get_rect(center=(center_x, center_y - s.font_size * 4.5))
        record_rect = record_msg.get_rect(center=(center_x, center_y - s.font_size * 3.5))
        s.screen.blit(msg, msg_rect)
        if type != 2:
            s.screen.blit(record_msg, record_rect)
        pg.display.update()
        
def main():
    pg.init()
    pg.font.init()
    
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    s.screen = screen
    pg.display.set_caption('Minesweeper')
    icon = pg.image.load('assets/icon.png')
    pg.display.set_icon(icon)

    dificulty = main_menu()
    game = Game(dificulty)
    
    clue_font = pg.font.SysFont(s.font_name, s.mini_font_size)
    info_font = pg.font.SysFont(s.font_name, s.font_size)
    record_font = pg.font.SysFont(s.font_name, s.font_size)
    
    clue_cords = [s.window[0] // 12, s.window[1] * 1.5]
    bomb_cords = (clue_cords[0], s.height // 2.25)
    flag_cords = (clue_cords[0], bomb_cords[1] + s.big_font_size)
    cur_record_cords = [s.window[0] * 1.20, s.window[1] // 4]
    best_record_cords = [s.window[0] + s.window[2] - cur_record_cords[0], cur_record_cords[1]]
    
    button_size = s.window[2] // 8
    stop_button_cords = [s.width - button_size - 15, 15, button_size, button_size]
    button_color = tuple(map(lambda x: x - 30, s.colors['screen']))
    
    clues = ['LMB - open', 'RMB - put/remove', 'flag']
    cur, best = f'Record - {game.record}', f'Best - 0'
    bomb = pg.image.load('assets/bomb.png').convert_alpha()
    flag = pg.image.load('assets/flag.png').convert_alpha()
    pause = pg.image.load('assets/pause.png').convert_alpha()
    
    mini_bomb = pg.transform.scale(bomb, (s.big_font_size, s.big_font_size))
    mini_flag = pg.transform.scale(flag, (s.big_font_size, s.big_font_size))
    mini_pause = pg.transform.scale(pause, (button_size, button_size))
    
    available_side = min(s.window[2], s.window[3])
    s.cell_size = max(1, (available_side - s.line_width * (game.game_field.size - 1)) // game.game_field.size)
    
    while game.running:
        screen.fill(SCREEN_COLOR)
        
        pg.draw.rect(screen, FRAME_COLOR, s.window)
        pg.draw.rect(screen, button_color, stop_button_cords, border_radius=10)
        pg.draw.rect(screen, tuple(map(lambda x: x - 30, button_color)), stop_button_cords, width=3, border_radius=10)

        draw_lines(screen, game.game_field.size, s.cell_size)
        s.screen.blit(mini_pause, stop_button_cords[:2])
        s.screen.blit(clue_font.render(clues[0], True, s.colors['text']), clue_cords)
        s.screen.blit(clue_font.render(clues[1], True, s.colors['text']), [clue_cords[0], clue_cords[1] + s.mini_font_size * 2])
        s.screen.blit(clue_font.render(clues[2], True, s.colors['text']), [clue_cords[0], clue_cords[1] + s.mini_font_size * 4])
        s.screen.blit(record_font.render(cur, True, s.colors['text']), cur_record_cords)
        s.screen.blit(record_font.render(best, True, s.colors['text']), best_record_cords)
        s.screen.blit(mini_bomb, bomb_cords)
        s.screen.blit(mini_flag, flag_cords)
        s.screen.blit(info_font.render(f' - {game.game_field.mines}', True, s.colors['text']), [bomb_cords[0] + s.big_font_size, bomb_cords[1]])
        s.screen.blit(info_font.render(f' - {game.flags}', True, s.colors['text']), [flag_cords[0] + s.big_font_size, flag_cords[1]])
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                game.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    game.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse = event.pos
                cord_x, cord_y = mouse[0] - s.window[0], mouse[1] - s.window[1]
                cell_x = int(cord_x // (s.cell_size + s.line_width))
                cell_y = int(cord_y // (s.cell_size + s.line_width))
                if (
                    0 <= cell_x < game.game_field.size and
                    0 <= cell_y < game.game_field.size and not
                    game.game_field.field[cell_x][cell_y].is_opened
                    ):
                    if event.button == 1:       
                        if game.opened_cells == 0:
                            game.mine_generate(cell_x, cell_y)
                        elif not game.game_field.field[cell_x][cell_y].has_flag:
                            new_cell = game.open_cell(cell_x, cell_y)
                            if new_cell.value == -1:
                                game.show_mines()
                                stop_game(game)
                            elif game.opened_cells == game.game_field.size ** 2 - game.game_field.mines:
                                game.record += 1
                                stop_game(game, 1)

                    elif event.button == 3:
                        if not game.game_field.field[cell_x][cell_y].has_flag:
                            if game.flags > 0:
                                game.put_flag(cell_x, cell_y)
                        else:
                            game.remove_flag(cell_x, cell_y)
                elif (stop_button_cords[0] <= mouse[0] <= stop_button_cords[0] + stop_button_cords[2] and
                      stop_button_cords[1] <= mouse[1] <= stop_button_cords[1] + stop_button_cords[3]):
                    stop_game(game, 2)
        game.draw_field()
        pg.display.update()
                            
if __name__ == '__main__':
    main()