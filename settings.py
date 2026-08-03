from pygame import mixer, image
from pygame.mixer import Sound
from pygame.image import load

mixer.init()
class Settings:
    width = 800
    height = 600
    prev_width = width
    prev_height = height
    base_width = width
    base_height = height
    is_fulscreen = False
    screen = None
    current_difficulty = None
    colors = {'line': (169, 143, 45), 'frame': (255, 231, 138), 'screen': (227, 213, 161), 'text': (132, 113, 42)}
    extra_colors = {'line': (179,0,115), 'frame': (255,103,25), 'screen': (83, 9, 9), 'text': (179,0,115)}
    field_params = {'easy': (9, 10), 'medium': (16, 35), 'hard': (20, 80)}
    time_params = {'easy': 5, 'medium': 90, 'hard': 180}
    cruel_mode = False
    line_width = 4
    font_size = 32
    mini_font_size = 16
    big_font_size = 48
    base_font_size = font_size
    base_mini_font_size = mini_font_size
    base_big_font_size = big_font_size
    font_name = 'comic sans'
    
    @classmethod
    def font_scale(cls, width=None, height=None):
        if width is None or height is None:
            return
        scale = height / cls.base_height
        cls.font_size = max(1, int(cls.base_font_size * scale))
        cls.mini_font_size = max(1, int(cls.base_mini_font_size * scale))
        cls.big_font_size = max(1, int(cls.base_big_font_size * scale))

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
    

class IMG:
    icon = load('assets/icon.png')
    
    flag = load('assets/flag.png')
    bomb = load('assets/bomb.png')
    defeat = load('assets/cat.png')
    victory = load('assets/omniman.jpg')
    main = load('assets/main.jpg')
    
    home = load('assets/home.png')
    cont = load('assets/continue.png')
    retry = load('assets/retry.png')
    next = load('assets/next.png')
    pause = load('assets/pause.png')
    settings = load('assets/settings.png')
    
    music_on = load('assets/music_on.png')
    sound_on = load('assets/sound_on.png')
    music_off = load('assets/music_off.png')
    sound_off = load('assets/sound_off.png')
    
    other_flag = None
    other_bomb = None
    other_defeat = None
    other_victory = None
    other_main = None
    
    @classmethod
    def picture(cls, img):
        return cls.__dict__[img].convert_alpha()
        
    