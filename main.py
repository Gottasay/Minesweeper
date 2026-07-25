from classes import Game, Field
from exceptions import *
from settings import Settings as s
import pygame as pg
from draw_schemas import draw_text_button, is_button_pressed, draw_picture_button

clue_cords = [s.window[0] // 12, s.window[1] * 1.5]
bomb_cords = (clue_cords[0], s.height // 2.25)
flag_cords = (clue_cords[0], bomb_cords[1] + s.big_font_size)
cur_record_cords = [s.window[0] * 1.20, s.window[1] // 4]
best_record_cords = [s.window[0] + s.window[2] - cur_record_cords[0], cur_record_cords[1]]
flag_amount_cords = [flag_cords[0] + s.big_font_size, flag_cords[1]]

button_size = s.window[2] // 8
stop_button_cords = [s.width - button_size - 15, 15, button_size, button_size]
button_color = tuple(map(lambda x: x - 30, s.colors['screen']))

clues = ['LMB - open', 'RMB - put/remove', 'flag']
            
def choose_dificulty():
    new_call = True
    button_color = tuple(map(lambda x: x - 50, s.colors['screen']))
    but_size, mess_size = 35, 50
    mess_font = pg.font.SysFont(s.font_name, mess_size)
    
    BUTTON_WIDTH = s.width // 5
    BUTTON_HEIGHT = s.height // 6
    OFFSET_Y = int(s.height * (2 / 3))
    DISTANCE = s.width // 10
    choose_msg = 'Choose difficulty:'
    message = mess_font.render(choose_msg, True , s.colors['text'])
    difs = ['easy', 'medium', 'hard']
    button_cords = []
    params = [(9, 10), (16, 35), (20, 80)]
    while True:
        mouse = pg.mouse.get_pos()
        if new_call:
            s.screen.fill(s.colors['screen'])
            s.screen.blit(message, ((s.width - len(choose_msg) * mess_size // 2) // 2, s.height // 3))
            dist = DISTANCE
            for dif in difs:
                cord = (dist, OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
                draw_text_button(
                    s.screen, button_color, cord,
                    border_radius=10, msg=dif, msg_size=but_size, width=2,
                    line_color=tuple(map(lambda x: x - 50, button_color))
                    )
                dist += DISTANCE + BUTTON_WIDTH
                button_cords.append(cord)
            new_call = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for but in range(3):
                    if is_button_pressed(mouse, button_cords[but]):
                        pg.mixer.Sound('sounds/button.wav').play()
                        return params[but]
        
        pg.display.update()

def main_menu():
    msg = 'Welcome to Minesweeper!'
    play_msg = 'Start'
    
    msg_size, play_size = 50, 40
    msg_font = pg.font.SysFont(s.font_name, msg_size)
    
    msg_cords = (s.width - len(msg) * msg_size // 2) // 2, s.height // 12
    play_button_cords = [s.width // 4, s.height * 3 // 4, s.width // 2, s.height // 10]
    picture_cords = [s.width // 4, s.height // 5, s.width // 2, s.height // 2]
    
    picture = pg.image.load('assets/main.jpg').convert_alpha()
    mini_picture = pg.transform.scale(picture, picture_cords[2:])
    play_button_color = tuple(map(lambda x: x - 25, s.colors['screen']))
    
    pg.mixer.music.load('music/meatball.wav')
    pg.mixer.music.play(-1)
    while True:
        s.screen.fill(s.colors['screen'])
        mouse = pg.mouse.get_pos()
        s.screen.blit(msg_font.render(msg, True, s.colors['text']), msg_cords)
        s.screen.blit(mini_picture, picture_cords[:2])
        draw_text_button(
            s.screen, play_button_color, play_button_cords,
            border_radius=10, msg=play_msg, msg_size=play_size, msg_orient='top', width=2,
            line_color=tuple(map(lambda x: x - 30, play_button_color))
                        )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if is_button_pressed(mouse, play_button_cords):
                    pg.mixer.Sound('sounds/button.wav').play()
                    return choose_dificulty()
        pg.display.update()    
                    
def draw_lines(screen, size, cell_size):
    left, top = s.window[0], s.window[1]
    width, height = s.window[2], s.window[3]

    for i in range(0, size + 1):
        x = left + i * (cell_size + s.line_width)
        y = top + i * (cell_size + s.line_width)
        pg.draw.line(screen, s.colors['line'], (x, top), (x, top + height), s.line_width)
        pg.draw.line(screen, s.colors['line'], (left, y), (left + width, y), s.line_width)


def stop_game(game, type=0):
    new_call = True
    end = {
        0: {'message': 'You lose!', 'main_pic': 'cat.png', 'button_set': ('home.png', 'retry.png')},
        1: {'message': 'You win!', 'main_pic': 'omniman.jpg', 'button_set': ('home.png', 'next.png')},
        2: {'message': 'Game paused!', 'main_pic': '', 'button_set': ('home.png', 'retry.png', 'continue.png')}}
    
    record = f'Your record: {game.record}'
    mess_font = pg.font.SysFont(s.font_name, s.font_size)
    record_msg = mess_font.render(record, True, s.colors['text'])
    
    x, y, a, b = s.width // 4, s.height // 4, s.width // 2, s.height // 1.8
    rect_cords = [x, y, a, b]
    button_1_cords = [x + a // 10, y + int(b * 23/30), a // 5, b // 5]
    button_2_cords = [x + int(a * 7/10), button_1_cords[1], a // 5, b // 5]
    main_pic_cords = [x + a // 4, y + b // 4, a // 2, b // 2]
    center_x = x + a // 2
    center_y = y + b // 2
    record_rect = record_msg.get_rect(center=(center_x, center_y - s.font_size * 3.5))
    
    rect_color = s.colors['screen']
    button_color = tuple(map(lambda x: x - 30, s.colors['screen']))
    
    pref = 'assets/'
    home_pic = pg.transform.scale(pg.image.load(pref + end[type]['button_set'][0]).convert_alpha(), button_1_cords[2:])
    refresh_pic = pg.transform.scale(pg.image.load(pref + end[type]['button_set'][1]).convert_alpha(), button_2_cords[2:])
    main_pic = pg.transform.scale(pg.image.load(pref + end[type]['main_pic']).convert_alpha(), main_pic_cords[2:]) if end[type]['main_pic'] else None
    while True:
        if new_call:
            game.draw_field()
            new_call = False    
            draw_text_button(
                s.screen, rect_color, rect_cords,
                border_radius=10, msg=end[type]['message'], msg_orient='top', width=5,
                line_color=button_color
                )
            draw_picture_button(
                s.screen, button_color, button_1_cords,
                picture=home_pic, width=5,
                line_color=tuple(map(lambda x: x - 30, button_color))
                )
            draw_picture_button(
                s.screen, button_color, button_2_cords,
                picture=refresh_pic, width=5,
                line_color=tuple(map(lambda x: x - 30, button_color))
                )
            if type == 0:
                pg.mixer.Sound('sounds/cat.wav').play()
                game.record = 0
                s.screen.blit(record_msg, record_rect)
            elif type == 1:
                pg.mixer.Sound('sounds/victory.wav').play()
                s.screen.blit(record_msg, record_rect)
            else:
                continue_pic = pg.transform.scale(pg.image.load(pref + end[type]['button_set'][2]).convert_alpha(), button_2_cords[2:])
                button_3_cords = [(button_1_cords[0] + button_2_cords[0]) // 2, button_1_cords[1], a // 5, b // 5]
                draw_picture_button(
                    s.screen, button_color, button_3_cords,
                    picture=continue_pic, width=5,
                    line_color=tuple(map(lambda x: x - 30, button_color))
                    )
            if main_pic:
                s.screen.blit(main_pic, main_pic_cords[:2])
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
                if is_button_pressed(mouse, button_1_cords):
                    pg.mixer.Sound('sounds/button.wav').play()
                    main()
                elif is_button_pressed(mouse, button_2_cords):
                    pg.mixer.Sound('sounds/button.wav').play()
                    game.reset()
                    return
                elif type == 2 and (is_button_pressed(mouse, button_3_cords) or is_button_pressed(mouse, stop_button_cords)):
                    pg.mixer.Sound('sounds/button.wav').play()
                    game.is_new = True
                    return
        pg.display.update()
        
def main():
    pg.init()
    pg.font.init()
    pg.mixer.init()
    
    screen = pg.display.set_mode((s.width, s.height))
    s.screen = screen
    pg.display.set_caption('Minesweeper')
    icon = pg.image.load('assets/icon.png')
    pg.display.set_icon(icon)
    
    dificulty = main_menu()
    game = Game(dificulty)
    
    
    bomb = pg.image.load('assets/bomb.png').convert_alpha()
    flag = pg.image.load('assets/flag.png').convert_alpha()
    pause = pg.image.load('assets/pause.png').convert_alpha()
    
    mini_bomb = pg.transform.scale(bomb, (s.big_font_size, s.big_font_size))
    mini_flag = pg.transform.scale(flag, (s.big_font_size, s.big_font_size))
    mini_pause = pg.transform.scale(pause, (button_size, button_size))
    
    clue_font = pg.font.SysFont(s.font_name, s.mini_font_size)
    info_font = pg.font.SysFont(s.font_name, s.font_size)
    record_font = pg.font.SysFont(s.font_name, s.font_size)
    
    available_side = min(s.window[2], s.window[3])
    s.cell_size = max(1, (available_side - s.line_width * (game.game_field.size - 1)) // game.game_field.size)
    while game.running:
        cur = f'Record - {game.record}'
        pg.draw.rect(screen, s.colors['screen'], [*flag_amount_cords, s.big_font_size * 1.75, s.big_font_size])
        s.screen.blit(info_font.render(f' - {game.flags}', True, s.colors['text']), flag_amount_cords)
        if game.is_new:
            pg.mixer.music.pause()
            best = game.get_best_result()
            best_msg = f'Best - {best}'
            
            screen.fill(s.colors['screen'])
            pg.draw.rect(screen, s.colors['frame'], s.window)
            draw_lines(screen, game.game_field.size, s.cell_size)
            
            draw_picture_button(
                s.screen, button_color, stop_button_cords,
                border_radius=10, picture=mini_pause, width=3,
                line_color=tuple(map(lambda x: x - 30, button_color))
                            )
            s.screen.blit(clue_font.render(clues[0], True, s.colors['text']), clue_cords)
            s.screen.blit(clue_font.render(clues[1], True, s.colors['text']), [clue_cords[0], clue_cords[1] + s.mini_font_size * 2])
            s.screen.blit(clue_font.render(clues[2], True, s.colors['text']), [clue_cords[0], clue_cords[1] + s.mini_font_size * 4])
            s.screen.blit(record_font.render(cur, True, s.colors['text']), cur_record_cords)
            s.screen.blit(record_font.render(best_msg, True, s.colors['text']), best_record_cords)
            s.screen.blit(mini_bomb, bomb_cords)
            s.screen.blit(mini_flag, flag_cords)
            s.screen.blit(info_font.render(f' - {game.game_field.mines}', True, s.colors['text']), [bomb_cords[0] + s.big_font_size, bomb_cords[1]])
            game.draw_field()
            game.is_new = False
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
                            pg.mixer.Sound('sounds/button.wav').play()
                            if new_cell.value == -1:
                                game.show_mines()
                                stop_game(game)
                            elif game.opened_cells == game.game_field.size ** 2 - game.game_field.mines:
                                game.record += 1
                                if game.record > best:
                                    game.change_result()
                                stop_game(game, 1)
                    elif event.button == 3:
                        if not game.game_field.field[cell_x][cell_y].has_flag:
                            if game.flags > 0:
                                game.put_flag(cell_x, cell_y)
                        else:
                            game.remove_flag(cell_x, cell_y)
                elif is_button_pressed(mouse, stop_button_cords):
                    pg.mixer.Sound('sounds/pause.wav').play()
                    stop_game(game, 2)
        pg.display.update()
                            
if __name__ == '__main__':
    main()