import pygame as pg
from settings import Settings as s
from settings import SFX as sfx
from settings import MessageScreen as m
from settings import PlayWindow as p
from settings import IMG as img

def draw_lines(screen, size):
    left, top, side = p.window[0], p.window[1], p.window[2]
    for i in range(0, size + 1):
        x = left + i * (p.cell_size + s.line_width)
        y = top + i * (p.cell_size + s.line_width)
        pg.draw.line(screen, s.colors['line'],
                     (x, top), (x, top + side), s.line_width)
        pg.draw.line(screen, s.colors['line'],
                     (left, y), (left + side, y), s.line_width)
    pg.draw.line(s.screen, s.colors['screen'], (x + s.line_width * 2, top -
                 s.line_width), (x + s.line_width * 2, top + side + s.line_width), 10)
    pg.draw.line(s.screen, s.colors['screen'], (left - s.line_width, y +
                 s.line_width * 2), (left + side + s.line_width, y + s.line_width * 2), 10)


def draw_text_button(surface,
                     color,
                     rect,
                     msg: str,
                     msg_size: int = s.font_size,
                     msg_color: tuple[int] = s.colors['text'],
                     msg_orient='center',
                     width: int = 0,
                     line_color: tuple[int] = (0, 0, 0),
                     border_radius: int = -1,
                     border_top_left_radius: int = -1,
                     border_top_right_radius: int = -1,
                     border_bottom_left_radius: int = -1,
                     border_bottom_right_radius: int = -1,
                     ):
    pg.draw.rect(
        surface=surface, color=color, rect=rect, border_radius=border_radius, border_top_left_radius=border_top_left_radius,
        border_top_right_radius=border_top_right_radius, border_bottom_left_radius=border_bottom_left_radius,
        border_bottom_right_radius=border_bottom_right_radius
    )
    pg.draw.rect(
        surface, line_color, rect, width, border_radius, border_top_left_radius,
        border_top_right_radius, border_bottom_left_radius,
        border_bottom_right_radius
    )
    message = pg.font.SysFont(
        s.font_name, msg_size).render(msg, True, msg_color)
    msg_cords = {
        'left': None,
        'right': None,
        'top': [rect[0] + (rect[2] - len(msg) * msg_size // 2) // 2, rect[1]],
        'center': [rect[0] + (rect[2] - len(msg) * msg_size // 2) // 2,
                   rect[1] + (rect[3] - msg_size) // 4]
    }
    surface.blit(message, msg_cords[msg_orient])


def draw_picture_button(
    surface,
    color,
    rect,
    picture,
    width: int = 0,
    line_color: tuple[int] = (0, 0, 0),
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1
):
    pg.draw.rect(
        surface=surface, color=color, rect=rect, border_radius=border_radius, border_top_left_radius=border_top_left_radius,
        border_top_right_radius=border_top_right_radius, border_bottom_left_radius=border_bottom_left_radius,
        border_bottom_right_radius=border_bottom_right_radius
    )
    pg.draw.rect(
        surface, line_color, rect, width, border_radius, border_top_left_radius,
        border_top_right_radius, border_bottom_left_radius,
        border_bottom_right_radius
    )
    surface.blit(picture, rect[:2])


def is_button_pressed(mouse, cords):
    return (cords[0] <= mouse[0] <= cords[0] + cords[2] and
            cords[1] <= mouse[1] <= cords[1] + cords[3])


def draw_sfx_lines():
    sound_cords = [m.rect[0] + m.rect[2] // 10, m.rect[1] +
                   m.rect[3] // 4, m.rect[2] // 6, m.rect[3] // 6]
    music_cords = [m.rect[0] + m.rect[2] // 10, m.rect[1] +
                   m.rect[3] // 2, m.rect[2] // 6, m.rect[3] // 6]
    s_x1, s_y1 = sound_cords[0] + sound_cords[2] + \
        10, sound_cords[1] + sound_cords[3] // 2
    s_x2, s_y2 = m.rect[0] + m.rect[2] - \
        sound_cords[2], sound_cords[1] + sound_cords[3] // 2
    m_x1, m_y1 = music_cords[0] + music_cords[2] + \
        10, music_cords[1] + music_cords[3] // 2
    m_x2, m_y2 = m.rect[0] + m.rect[2] - \
        music_cords[2], music_cords[1] + music_cords[3] // 2
    rad = 8
    pg.draw.rect(s.screen, s.colors['screen'], (s_x1 - rad,
                 s_y1 - rad * 2, s_x2 - s_x1 + rad * 2, rad * 3))
    pg.draw.rect(s.screen, s.colors['screen'], (m_x1 - rad,
                 m_y1 - rad * 2, m_x2 - m_x1 + rad * 2, rad * 3))
    pg.draw.line(
        s.screen,
        (255, 0, 0),
        (s_x1, s_y1), (s_x2, s_y2),
        width=5
    )
    pg.draw.line(
        s.screen,
        (0, 255, 0),
        (m_x1, m_y1), (m_x2, m_y2),
        width=5
    )
    pg.draw.circle(s.screen, (255, 0, 0),
                   (s_x1 + (s_x2 - s_x1) * sfx.sound_volume, s_y2), rad)
    pg.draw.circle(s.screen, (0, 255, 0),
                   (m_x1 + (m_x2 - m_x1) * sfx.music_volume, m_y2), rad)
    return (s_x1, s_y1), (s_x2, s_y2), (m_x1, m_y1), (m_x2, m_y2)


def draw_sfx():
    sound_cords = [m.rect[0] + m.rect[2] // 10, m.rect[1] +
                   m.rect[3] // 4, m.rect[3] // 6, m.rect[3] // 6]
    music_cords = [m.rect[0] + m.rect[2] // 10, m.rect[1] +
                   m.rect[3] // 2, m.rect[3] // 6, m.rect[3] // 6]

    s_pic = img.picture('sound_on') if sfx.sound_volume > 0.03 else img.picture('sound_off')
    m_pic = img.picture('music_on') if sfx.music_volume > 0.03 else img.picture('music_off')

    sound = pg.transform.scale(s_pic, sound_cords[2:])
    music = pg.transform.scale(m_pic, music_cords[2:])

    pg.draw.rect(s.screen, s.colors['screen'], sound_cords)
    pg.draw.rect(s.screen, s.colors['screen'], music_cords)
    s.screen.blit(sound, sound_cords)
    s.screen.blit(music, music_cords)

    return draw_sfx_lines()


def draw_info(game):

    clue_font = pg.font.SysFont(s.font_name, s.mini_font_size)
    info_font = pg.font.SysFont(s.font_name, s.font_size)
    record_font = pg.font.SysFont(s.font_name, s.font_size)

    cur = f'Record - {game.record}'
    best_msg = f'Best - {game.best_record}'
    mini_bomb = pg.transform.scale(img.picture('bomb'), (s.big_font_size, s.big_font_size))
    mini_flag = pg.transform.scale(img.picture('flag'), (s.big_font_size, s.big_font_size))

    tab = p.window[2] // 18
    indent_left = s.width // 30

    clue_cords1 = [p.window[0] + tab, p.window[1] - s.mini_font_size * 2]
    clue_cords2 = [p.window[0] + tab * 2 +
                   15 * s.mini_font_size, clue_cords1[1]]
    bomb_cords = (indent_left, s.height // 2.25)
    flag_cords = (indent_left, bomb_cords[1] + s.big_font_size)
    cur_record_cords = [indent_left, s.height // 20]
    best_record_cords = [indent_left, cur_record_cords[1] + s.font_size * 2]
    flag_amount_cords = [flag_cords[0] + s.big_font_size, flag_cords[1]]

    s.screen.blit(clue_font.render('RMB - open cell',
                  True, s.colors['text']), clue_cords1)
    s.screen.blit(clue_font.render('LMB - put/reset flag',
                  True, s.colors['text']), clue_cords2)
    s.screen.blit(record_font.render(
        cur, True, s.colors['text']), cur_record_cords)
    s.screen.blit(record_font.render(best_msg, True,
                  s.colors['text']), best_record_cords)
    s.screen.blit(mini_bomb, bomb_cords)
    s.screen.blit(mini_flag, flag_cords)
    s.screen.blit(info_font.render(
        f' - {game.flags}', True, s.colors['text']), flag_amount_cords)
    s.screen.blit(info_font.render(f' - {game.game_field.mines}', True,
                  s.colors['text']), [bomb_cords[0] + s.big_font_size, bomb_cords[1]])


def draw_timer(timer: int):
    if timer < 0:
        return
    timer_font = pg.font.SysFont(s.font_name, s.font_size)
    timer_cords = [s.width // 2 - 3 * s.font_size // 2, s.height - s.font_size * 2]
    time_color = s.colors['text'] if timer > 15 else (255, 0, 0)
    total_seconds = max(0, int(timer))
    minutes, seconds = divmod(total_seconds, 60)
    s.screen.blit(timer_font.render(
        f'{minutes:02d}:{seconds:02d}', True, time_color), timer_cords)
