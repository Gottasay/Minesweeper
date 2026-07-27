from pygame import mixer
from pygame.mixer import Sound

mixer.init()
class Settings:
    width = 800
    height = 600
    cell_size = None
    screen = None
    colors = {'line': (169, 143, 45), 'frame': (255,231,138), 'screen': (227, 213, 161), 'text': (132, 113, 42)}
    line_width = 2
    font_size = 30
    mini_font_size = 16
    big_font_size = 50
    font_name = 'comic sans'
    window_side = width * 2 // 3 * 0.9
    window_x, window_y = (width - window_side) // 2, (height - window_side) // 2
    window = [window_x, window_y, window_side, window_side]

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
    rect = Settings.width // 4, Settings.height // 4, Settings.width // 2, Settings.height // 1.8
    color = Settings.colors['screen'],
    width = Settings.line_width
    line_color = tuple(map(lambda x: x - 30, Settings.colors['screen']))
    
