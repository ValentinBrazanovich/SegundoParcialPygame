import pygame
import config

class Slider:
    def __init__(self, pos, size, initial_val, min_val, max_val, on_update=None, on_draw=None):
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min_val
        self.max = max_val
        # porcentaje
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos,
                                          self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5,
                                       self.slider_top_pos, 10, self.size[1])

        self.on_update = on_update
        self.on_draw = on_draw
    
    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]
        if self.on_update:
            self.on_update()

    def render(self):
        config.screen.blit(config.slide_bar_img, self.container_rect.topleft)
        pygame.draw.circle(config.screen, "darkgray", self.button_rect.center, 20)
        pygame.draw.circle(config.screen, "gray", self.button_rect.center, 18)
        pygame.draw.circle(config.screen, "white", self.button_rect.center, 16)
        if self.on_draw:
            self.on_draw()

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return round((button_val / val_range) * (self.max - self.min) + self.min)