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
    extra_colors = {'line': (87,0,0), 'frame': (59,59,59), 'screen': (80,80,80), 'text': (117,0,0)}
    field_params = {'easy': (9, 10), 'medium': (16, 35), 'hard': (20, 80)}
    time_params = {'easy': 60, 'medium': 120, 'hard': 240}
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

    @classmethod
    def swapmode(cls):
        cls.cruel_mode = not cls.cruel_mode
        cls.colors, cls.extra_colors = cls.extra_colors, cls.colors
        SFX.swapmode()
        IMG.swapmode()
        MessageScreen.color = cls.colors['screen']
        PlayWindow.button_color = tuple(map(lambda x: x - 30, cls.colors['screen']))
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
       'reset_flag': Sound('sounds/boom.wav'),
       'button': Sound('sounds/button.wav'),
       'defeat': Sound('sounds/cat.wav'),
       'flag': Sound('sounds/eagle.wav'),
       'bomb': Sound('sounds/fart.wav'),
       'pause': Sound('sounds/pause.wav'),
       'victory': Sound('sounds/victory.wav'),
       'other_defeat': Sound('sounds/evil_laugh.wav'),
       'other_victory': Sound('sounds/excuse_me_sir.wav'),
       'other_flag': Sound('sounds/bark.wav'),
       'other_reset_flag': Sound('sounds/bonk.wav'),
       'other_bomb': Sound('sounds/fnaf.wav'),
    }
    music = {
        'main': 'music/meatball.wav',
        'other_main': 'music/paranoid.wav',
        'game': 'music/monkeys.wav',
        'other_game': 'music/eateot.wav'
             }
    
    @classmethod
    def set_volume(cls, sound_volume=None):
        for sound in cls.all_sounds.values():
            sound.set_volume(sound_volume)
            
    @classmethod
    def swapmode(cls):
        cls.all_sounds['flag'], cls.all_sounds['other_flag'] = cls.all_sounds['other_flag'], cls.all_sounds['flag']
        cls.all_sounds['bomb'], cls.all_sounds['other_bomb'] = cls.all_sounds['other_bomb'], cls.all_sounds['bomb']
        cls.all_sounds['defeat'], cls.all_sounds['other_defeat'] = cls.all_sounds['other_defeat'], cls.all_sounds['defeat']
        cls.all_sounds['victory'], cls.all_sounds['other_victory'] = cls.all_sounds['other_victory'], cls.all_sounds['victory']
        cls.all_sounds['reset_flag'], cls.all_sounds['other_reset_flag'] = cls.all_sounds['other_reset_flag'], cls.all_sounds['reset_flag']
        cls.music['main'], cls.music['other_main'] = cls.music['other_main'], cls.music['main']
        cls.music['game'], cls.music['other_game'] = cls.music['other_game'], cls.music['game']
    
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
    
    other_flag = load('assets/flag_bullterrier.png')
    other_bomb = load('assets/trollface.png')
    other_defeat = load('assets/holden.png')
    other_victory = load('assets/butcher.png')
    other_main = load('assets/main_cruel.png')
    
    @classmethod
    def picture(cls, img):
        return cls.__dict__[img].convert_alpha()
        
    @classmethod
    def swapmode(cls):
        cls.flag, cls.other_flag = cls.other_flag, cls.flag
        cls.bomb, cls.other_bomb = cls.other_bomb, cls.bomb
        cls.defeat, cls.other_defeat = cls.other_defeat, cls.defeat
        cls.victory, cls.other_victory = cls.other_victory, cls.victory
        cls.main, cls.other_main = cls.other_main, cls.main
