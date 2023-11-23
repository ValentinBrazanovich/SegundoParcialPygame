from config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = pygame.transform.scale(item_boxes[self.item_type], (scale))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +(TILE_SIZE - self.image.get_height()))

    def update(self, player):
        #colision con el item
        if pygame.sprite.collide_rect(self, player):
            #con que tipo de item colisiona
            if self.item_type == "Health":
                player.health += 40
                if player.health > player.max_health:
                    player.health = player.max_health
                health_sound.play()
                player.score += 15
            elif self.item_type == "Coin":
                coin_sound.play()
                player.score += 50
            elif self.item_type == "Ammo":
                player.ammunition += 10
                if player.ammunition > 50:
                    player.ammunition = 50
                ammo_sound.play()
                player.score += 10
            self.kill()