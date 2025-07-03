class GameScaler:
    def __init__(self, base_width, base_height, screen):
        self.base_width = base_width
        self.base_height = base_height
        self.screen = screen
        self.update_scale()

    def update_scale(self):
        screen_width, screen_height = self.screen.get_size()
        self.scale_x = screen_width / self.base_width
        self.scale_y = screen_height / self.base_height

    def scale_pos(self, x, y):
        return int(x * self.scale_x), int(y * self.scale_y)

    def scale_size(self, w, h):
        return int(w * self.scale_x), int(h * self.scale_y)

    def scale_font(self, font_size):
        return int(font_size * (self.scale_x + self.scale_y) / 2)

scaler = None

def set_scaler(s):
    global scaler
    scaler = s
    print("Scaler set:", scaler)