from config import *

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(img, scale)
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))