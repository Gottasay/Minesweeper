from classes import Game, Field
from exceptions import *
from settings import Settings as s
from settings import SFX as sfx
from settings import MessageScreen as m
from settings import PlayWindow as p
from settings import IMG as img
import pygame as pg
from draw_schemas import draw_text_button, is_button_pressed, draw_picture_button, draw_sfx, draw_lines, draw_info, draw_timer
from time import time

def change_volume(state, s_cords, m_cords):
    mouse = pg.mouse.get_pos()
    if state and s_cords[0][0] <= mouse[0] <= s_cords[1][0] and s_cords[0][1] - 10 <= mouse[1] <= s_cords[0][1] + 10:
        sfx.sound_volume = (mouse[0] - s_cords[0][0]) / (s_cords[1][0] - s_cords[0][0])
        sound_set(sfx.sound_volume)
    elif state and m_cords[0][0] <= mouse[0] <= m_cords[1][0] and m_cords[0][1] - 10 <= mouse[1] <= m_cords[0][1] + 10:
        sfx.music_volume = (mouse[0] - m_cords[0][0]) / (m_cords[1][0] - m_cords[0][0])
        pg.mixer.music.set_volume(sfx.music_volume)


def screen_changed():
    if s.screen is None:
        return
    cur_width, cur_height = s.screen.get_size()
    if cur_width != s.width or cur_height != s.height:
        s.width, s.height = cur_width, cur_height
        s.font_scale(width=s.width, height=s.height)
        p.button_size = s.height * 11 // 100
        p.settings_cords = [s.width - p.button_size - 15, 15, p.button_size, p.button_size]
        m_side = s.height // 1.8
        w_rect, w_mini = s.height * 2 // 3, s.height * 4 // 5
        m.rect = (s.width - w_rect) // 2, s.height // 4, w_rect, m_side
        m.mini_rect = (s.width - w_mini) // 2, s.height // 4, w_mini, m_side


def toggle_fullscreen(KF_11=False):
    if s.is_fulscreen:
        s.screen = pg.display.set_mode((s.prev_width, s.prev_height), pg.RESIZABLE)
        s.width, s.height, s.prev_width, s.prev_height = s.prev_width, s.prev_height, s.width, s.height
        s.font_scale(width=s.width, height=s.height)
        s.is_fulscreen = False
    else:
        s.prev_width, s.prev_height = s.width, s.height
        info = pg.display.Info()
        s.width, s.height = info.current_w, info.current_h
        if KF_11:
            s.screen = pg.display.set_mode((s.width, s.height), pg.FULLSCREEN)
        else:
            s.screen = pg.display.set_mode((s.width, s.height), pg.RESIZABLE)
        s.font_scale(width=s.width, height=s.height)
        s.is_fulscreen = True
    p.button_size = s.height * 11 // 100
    p.settings_cords = [s.width - p.button_size - 15, 15, p.button_size, p.button_size]
    m_side = s.height // 1.8
    w_rect, w_mini = s.height * 2 // 3, s.height * 4 // 5
    m.rect = (s.width - w_rect) // 2, s.height // 4, w_rect, m_side
    m.mini_rect = (s.width - w_mini) // 2, s.height // 4, w_mini, m_side
    
def game_parameters(redraw):
    sfx.all_sounds['button'].play()
    while True:
        screen_changed()
        redraw()
        mouse = pg.mouse.get_pos()
        draw_text_button(
            s.screen, m.color, m.mini_rect,
            border_radius=10, msg='Settings', msg_size=s.big_font_size,
            msg_orient='top', width=5, line_color=p.button_color
            )
        s1, s2, m1, m2 = draw_sfx()
        change_volume(pg.mouse.get_pressed()[0], (s1, s2), (m1, m2))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_F11:
                    toggle_fullscreen(KF_11=True)
            if event.type == pg.MOUSEBUTTONDOWN:
                if is_button_pressed(mouse, p.settings_cords):
                    return
        pg.display.update()
        
def choose_dificulty():
    choose_msg = 'Choose difficulty:'
    def redraw():
        mess_font = pg.font.SysFont(s.font_name, s.big_font_size)
        message = mess_font.render(choose_msg, True , s.colors['text'])
        settings_cords = [s.width - p.button_size - 15, 15, p.button_size, p.button_size]
        easy_cords = (s.width // 10, s.height * 2 // 3, s.width // 5, s.height // 6)
        medium_cords = (s.width // 10 * 2 + s.width // 5, s.height * 2 // 3, s.width // 5, s.height // 6)
        hard_cords = (s.width // 10 * 3 + s.width // 5 * 2, s.height * 2 // 3, s.width // 5, s.height // 6)
        settings = pg.transform.scale(img.picture('settings'), (p.button_size, p.button_size))
        s.screen.fill(s.colors['screen'])
        s.screen.blit(message, ((s.width - len(choose_msg) * s.big_font_size // 2) // 2, s.height // 3))
        draw_picture_button(
            s.screen, p.button_color, settings_cords,
            border_radius=10, picture=settings, width=3,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
                        ) 
        draw_text_button(
            s.screen, p.button_color, easy_cords,
            border_radius=10, msg='Easy', msg_size=s.font_size, msg_orient='center',
            width=2, line_color=tuple(map(lambda x: x - 50, p.button_color))
            )
        draw_text_button(
            s.screen, p.button_color, medium_cords,
            border_radius=10, msg='Medium', msg_size=s.font_size, msg_orient='center',
            width=2,line_color=tuple(map(lambda x: x - 50, p.button_color))
            )
        draw_text_button(
            s.screen, p.button_color, hard_cords,
            border_radius=10, msg='Hard', msg_size=s.font_size, msg_orient='center',
            width=2, line_color=tuple(map(lambda x: x - 50, p.button_color))
            )
        return easy_cords, medium_cords, hard_cords
    while True:
        screen_changed()
        mouse = pg.mouse.get_pos()
        easy_cords, medium_cords, hard_cords = redraw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_F11:
                    toggle_fullscreen(KF_11=True)
            if event.type == pg.MOUSEBUTTONDOWN:
                if is_button_pressed(mouse, p.settings_cords):
                    game_parameters(redraw)
                if is_button_pressed(mouse, easy_cords):
                    sfx.all_sounds['button'].play()
                    s.current_difficulty = 'easy'
                    return s.field_params[s.current_difficulty]
                if is_button_pressed(mouse, medium_cords):
                    sfx.all_sounds['button'].play()
                    s.current_difficulty = 'medium'
                    return s.field_params[s.current_difficulty]
                if is_button_pressed(mouse, hard_cords):
                    sfx.all_sounds['button'].play()
                    s.current_difficulty = 'hard'
                    return s.field_params[s.current_difficulty]
        
        pg.display.update()


def main_menu():
    msg = 'Welcome to Minesweeper!'
    play_msg = 'Start'
    mode_msg = 'Hardmode'
    picture = img.picture('main')
    pg.mixer.music.load('music/meatball.wav')
    pg.mixer.music.play(-1)
    def redraw():
        msg_font = pg.font.SysFont(s.font_name, s.big_font_size)
        msg_cords = (s.width - len(msg) * s.big_font_size // 2) // 2, s.height // 12
        pb_width, pic_width = s.height * 2 // 3, s.height * 2 // 3
        play_button_cords = [(s.width - pb_width) // 2, s.height * 2.2 // 3, pb_width, s.height // 10]
        change_mode_cords = [play_button_cords[0], play_button_cords[1] + play_button_cords[3] + 20, play_button_cords[2], play_button_cords[3]]
        picture_cords = [(s.width - pic_width) // 2, s.height // 5, pic_width, s.height // 2]
        mini_picture = pg.transform.scale(picture, picture_cords[2:])  
        settings = pg.transform.scale(img.picture('settings'), (p.button_size, p.button_size))
        s.screen.fill(s.colors['screen'])
        s.screen.blit(msg_font.render(msg, True, s.colors['text']), msg_cords)
        s.screen.blit(mini_picture, picture_cords[:2])
        draw_text_button(
            s.screen, p.button_color, play_button_cords,
            border_radius=10, msg=play_msg, msg_size=s.font_size, msg_orient='center', width=2,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
                        )
        draw_text_button(
            s.screen, p.button_color, change_mode_cords,
            border_radius=10, msg=mode_msg, msg_size=s.font_size, msg_orient='center', width=2,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
                        )
        draw_picture_button(
            s.screen, p.button_color, p.settings_cords,
            border_radius=10, picture=settings, width=3,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
                        )
        return play_button_cords, change_mode_cords
    while True:
        screen_changed()
        play_button_cords, change_mode_cords = redraw()[0], redraw()[1]
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_F11:
                    s.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                    toggle_fullscreen(KF_11=True)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if is_button_pressed(mouse, play_button_cords):
                    sfx.all_sounds['button'].play()
                    return choose_dificulty()
                elif is_button_pressed(mouse, change_mode_cords):
                    s.colors, s.extra_colors = s.extra_colors, s.colors
                    s.cruel_mode = not s.cruel_mode
                    # redraw()
                elif is_button_pressed(mouse, p.settings_cords):
                    game_parameters(redraw)
                        
        pg.display.update()    
                    

def stop_game(game, redraw, type=0, timer=None):
    end = {
        0: {'message': 'You lose!', 'main_pic': 'defeat', 'button_set': ('home', 'retry')},
        1: {'message': 'You win!', 'main_pic': 'victory', 'button_set': ('home', 'next')},
        2: {'message': 'Game paused!', 'main_pic': '', 'button_set': ('home', 'retry', 'cont')}}
    
    record = f'Your record: {game.record}'
    first_call = True
    if type == 2 and s.cruel_mode:
        pause_time = time()
    while True:
        screen_changed()
        redraw()
        if s.cruel_mode:
            draw_timer(timer)
        x, y, a, b = m.rect
        rect_cords = [x, y, a, b]
        button_1_cords = [x + a // 10, y + int(b * 23/30), b // 5, b // 5]
        button_2_cords = [x + a - a // 10 - b // 5, button_1_cords[1], b // 5, b // 5]
        pic_width = b // 2
        main_pic_cords = [(a - pic_width) // 2 + x, y + b // 4, pic_width, pic_width]
        center_x = x + a // 2
        center_y = y + b // 2
        mess_font = pg.font.SysFont(s.font_name, s.font_size)
        record_msg = mess_font.render(record, True, s.colors['text'])
        record_rect = record_msg.get_rect(center=(center_x, center_y - s.font_size * 3.5))
        
        home_pic = pg.transform.scale(img.picture(end[type]['button_set'][0]), button_1_cords[2:])
        refresh_pic = pg.transform.scale(img.picture(end[type]['button_set'][1]), button_2_cords[2:])
        main_pic = pg.transform.scale(img.picture(end[type]['main_pic']), main_pic_cords[2:]) if end[type]['main_pic'] else None
            
        draw_text_button(
            s.screen, m.color, rect_cords,
            border_radius=10, msg=end[type]['message'], msg_size=s.font_size,
            msg_orient='top', width=5, line_color=p.button_color
            )
        draw_picture_button(
            s.screen, p.button_color, button_1_cords,
            picture=home_pic, width=5,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
            )
        draw_picture_button(
            s.screen, p.button_color, button_2_cords,
            picture=refresh_pic, width=5,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
            )
        if type == 0:
            if first_call:
                sfx.all_sounds['cat'].play()
                first_call = False
            game.record = 0
            s.screen.blit(record_msg, record_rect)
        elif type == 1:
            if first_call:
                sfx.all_sounds['victory'].play()
                first_call = False
            s.screen.blit(record_msg, record_rect)
        else:
            continue_pic = pg.transform.scale(img.picture(end[type]['button_set'][2]), button_2_cords[2:])
            button_3_cords = [(button_1_cords[0] + button_2_cords[0]) // 2, button_1_cords[1], b // 5, b // 5]
            draw_picture_button(
                s.screen, p.button_color, button_3_cords,
                picture=continue_pic, width=5,
                line_color=tuple(map(lambda x: x - 30, p.button_color))
                )
            s1, s2, m1, m2 = draw_sfx()
        if main_pic:
            s.screen.blit(main_pic, main_pic_cords[:2])
        
        mouse_button = pg.mouse.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                game.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    game.running = False
                if event.key == pg.K_F11:
                    toggle_fullscreen(KF_11=True)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse = event.pos
                if is_button_pressed(mouse, button_1_cords):
                    sfx.all_sounds['button'].play()
                    main()
                elif is_button_pressed(mouse, button_2_cords):
                    sfx.all_sounds['button'].play()
                    game.reset()
                    return
                elif type == 2 and (is_button_pressed(mouse, button_3_cords) or is_button_pressed(mouse, p.settings_cords)):
                    sfx.all_sounds['button'].play()
                    if s.cruel_mode:
                        game.expire_time += time() - pause_time
                    game.is_new = True
                    return
        if type == 2:
            change_volume(mouse_button[0], (s1, s2), (m1, m2))
            draw_sfx()
        pg.display.update()

def sound_set(value):
    for sound in sfx.all_sounds.values():
        sound.set_volume(value)
   
def main():
    pg.init()
    pg.font.init()
    pg.mixer.init()
    s.screen = pg.display.set_mode((s.width, s.height), pg.RESIZABLE)
    pg.display.set_caption('Minesweeper')
    icon = img.picture('icon')
    pg.display.set_icon(icon)
    dificulty = main_menu()
    game = Game(dificulty)
    
    pause = img.picture('pause')
    pg.mixer.music.set_volume(sfx.music_volume)
    sound_set(sfx.sound_volume)
    pg.mixer.music.load('music/monkeys.wav')
    pg.mixer.music.play(-1)
    if s.cruel_mode:
        game.expire_time = time() + s.time_params[s.current_difficulty]
    
    def redraw():
        mini_pause = pg.transform.scale(pause, (p.button_size, p.button_size))
        p.window_side = s.height * 3 // 4
        p.window_x, p.window_y = (s.width - p.window_side) // 2, (s.height - p.window_side) // 2
        p.window = [p.window_x, p.window_y, p.window_side, p.window_side]
        p.cell_size = max(1, (p.window[2] - s.line_width * (game.game_field.size - 1)) // game.game_field.size)      
        s.screen.fill(s.colors['screen'])
        pg.draw.rect(s.screen, s.colors['frame'], p.window)
        draw_lines(s.screen, game.game_field.size)
        
        draw_picture_button(
            s.screen, p.button_color, p.settings_cords,
            border_radius=10, picture=mini_pause, width=3,
            line_color=tuple(map(lambda x: x - 30, p.button_color))
                        )
        draw_info(game)
        game.draw_field()
        
    while game.running:
        screen_changed()
        redraw()
        if s.cruel_mode:
            time_left = game.expire_time - time()
            draw_timer(time_left)
            if time_left <= 0:
                game.show_mines()
                stop_game(game, redraw=redraw, timer=0)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                game.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    game.running = False
                if event.key == pg.K_F11:
                    toggle_fullscreen(KF_11=True)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse = event.pos
                cord_x, cord_y = mouse[0] - p.window[0], mouse[1] - p.window[1]
                cell_x = int(cord_x // (p.cell_size + s.line_width))
                cell_y = int(cord_y // (p.cell_size + s.line_width))
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
                            sfx.all_sounds['button'].play()
                            if new_cell.value == -1:
                                game.show_mines()
                                timer = game.expire_time - time() if game.expire_time else None
                                stop_game(game, redraw=redraw, timer=timer)
                            elif game.opened_cells == game.game_field.size ** 2 - game.game_field.mines:
                                game.record += 1
                                if game.record > game.best_record:
                                    game.change_result()
                                timer = game.expire_time - time() if game.expire_time else None
                                stop_game(game, redraw=redraw, type=1, timer=timer)
                    elif event.button == 3:
                        if not game.game_field.field[cell_x][cell_y].has_flag:
                            if game.flags > 0:
                                game.put_flag(cell_x, cell_y)
                        else:
                            game.remove_flag(cell_x, cell_y)
                elif is_button_pressed(mouse, p.settings_cords):
                    sfx.all_sounds['pause'].play()
                    time_left = game.expire_time - time() if game.expire_time else None
                    stop_game(game, redraw=redraw, type=2, timer=time_left)
        pg.display.update()
                            
if __name__ == '__main__':
    main()