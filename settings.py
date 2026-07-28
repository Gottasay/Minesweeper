from pygame import mixer
from pygame.mixer import Sound

mixer.init()
class Settings:
    width = 800
    height = 600
    prev_width = 0
    prev_height = 0
    is_fulscreen = False
    screen = None
    colors = {'line': (169, 143, 45), 'frame': (255, 231, 138), 'screen': (227, 213, 161), 'text': (132, 113, 42)}
    line_width = 4
    font_size = 30
    mini_font_size = 16
    big_font_size = 50
    font_name = 'comic sans'

class PlayWindow:
    window_side = Settings.width * 2 // 3
    window_x, window_y = (Settings.width - window_side) // 2, (Settings.height - window_side) // 2
    window = [window_x, window_y, window_side, window_side]
    button_size = window[2] // 8
    button_color = tuple(map(lambda x: x - 30, Settings.colors['screen']))
    settings_cords = [Settings.width - button_size - 15, 15, button_size, button_size]
    cell_size = None
    
class SFX:
    sound_volume = 1.0
    music_volume = 1.0
    all_sounds = {
       'boom': Sound('sounds/boom.wav'),
       'button': Sound('sounds/button.wav'),
       'cat': Sound('sounds/cat.wav'),
       'eagle': Sound('sounds/eagle.wav'),
       'fart': Sound('sounds/fart.wav'),
       'pause': Sound('sounds/pause.wav'),
       'victory': Sound('sounds/victory.wav') 
    }
    
class MessageScreen:
    rect = Settings.width // 4, Settings.height // 4, Settings.height * 2 // 3, Settings.height // 1.8
    mini_rect = Settings.width // 5, Settings.height // 4, Settings.height * 4 // 5, Settings.height // 1.8
    color = Settings.colors['screen'],
    width = Settings.line_width
    line_color = tuple(map(lambda x: x - 30, Settings.colors['screen']))
    
