from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img, damage):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.damage = damage
        self.can_damage_stormtrooper = True

    def update(self, player, world):
        #muevo la bala
        self.rect.x += (self.direction * self.speed)

        #si las balas se salen de la pantalla desaparecen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        #colision con los bloques
        for tile in world.platform_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #colision con los enemigos
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= self.damage
                player.score -= 15
                self.kill()
        for stormtrooper in stormtrooper_group:
            if pygame.sprite.spritecollide(stormtrooper, bullet_group, False):
                if stormtrooper.alive and self.can_damage_stormtrooper:
                    stormtrooper.health -= 35
                    player.score += 15
                    self.kill()                  
        for arachnid in arachnid_group:
            if pygame.sprite.spritecollide(arachnid, bullet_group, False):
                if arachnid.alive:
                    arachnid.health -= 30
                    player.score += 20
                    self.kill()
        for boss in boss_group:
            if pygame.sprite.spritecollide(boss, bullet_group, False):
                if boss.alive:
                    boss.health -= 20
                    player.score += 50
                    self.kill()
        #El puntaje no puede ser negativo
        if player.score < 0:
            player.score = 0