from config import *

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, bar_width, bar_height):
        #actualizar barra de vida
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, "dimgray", (self.x - 2, self.y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, "red", (self.x, self.y, bar_width, bar_height))
        pygame.draw.rect(screen, "lightblue", (self.x, self.y, bar_width * ratio, bar_height))