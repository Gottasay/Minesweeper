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
