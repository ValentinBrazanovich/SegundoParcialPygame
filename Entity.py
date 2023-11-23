from config import *
#############################
from Bullet import *


import os

class Entity(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammunition, health):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammunition = ammunition
        self.start_ammunition = ammunition
        self.shoot_cooldown = 0
        self.health = health
        self.max_health = self.health
        self.direction = -1
        self.vel_y = 0
        self.death_sound_played = False
        self.in_air = True
        self.jump = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.score = 0
        self.vision = pygame.Rect(0, 0, 250, 40)
        self.update_time = pygame.time.get_ticks()
        self.level_completed = False

        #cargar sprites segun acion
        animation_types = ["Quieto", "Camina", "Salta", "Dispara", "Muere"]
        for animation in animation_types:

            temp_list = []

            #cuenta la cantidad de archivos en la carpeta
            cant_frames = len(os.listdir(f'Recursos/{self.char_type}/{animation}'))
            for num in range(cant_frames):
                img = pygame.image.load(f'Recursos/{self.char_type}/{animation}/{num}.png')
                if self.char_type == "Stormtrooper" and animation == "Muere":
                    img = pygame.transform.scale(img, (60, 60))
                else:
                    img = pygame.transform.scale(img, (scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        
        #al colisionar con lava, la entidad pierde vida constantemente
        if pygame.sprite.spritecollide(self, lava_group, False):
            self.health -= 3


        #si el jugador toca al mecha aracnido pierde vida
        arachnid_collisions = pygame.sprite.spritecollide(self, arachnid_group, False)
        for arachnid in arachnid_group:
            if arachnid_collisions and arachnid.health > 0:
                if self.char_type == "Solo":
                    self.health -= 1
        #Si se colisiona con la salida, se puede avanzar de nivel
        exit_collisions = pygame.sprite.spritecollide(self, exit_group, False)
        if exit_collisions:
            self.level_completed = True

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, mover_izq, mover_der, world):
        #se resetean las variables de movimiento
        dx = 0
        dy = 0
        if mover_izq:
            dx = -self.speed 
            self.flip = True
            self.direction = -1
        if mover_der:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #salto
        if self.jump and not self.in_air:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        #gravedad
        self.vel_y += GRAVEDAD
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #colision con las plataformas
        for tile in world.platform_list:
            #colision en eje x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #Si la ia choca con una pared, se da vuelta
                if not self.char_type == "Solo":
                    self.direction *= -1
                    self.move_counter = 0
            if self.char_type == "Stormtrooper":
                if tile[1].colliderect(self.rect.x + dx + 1, self.rect.y, self.width, self.height):
                    dx = 0
                    #Si la ia choca con una pared, se da vuelta
                    self.direction *= -1
                    self.move_counter = 0
            #colision en eje y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #si choca el top del personaje con el bottom de un bloque
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    #si choca el bottom del personaje con el top del bloque
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
            #si esta en el aire no puede saltar
            if self.vel_y > 0:
                self.in_air = True
                    

        #colision con los bordes de la pantalla
        if self.rect.x < 0:
                self.rect.x = 0
        if self.rect.x > WIDTH - self.width:
            self.rect.x = WIDTH - self.width
        #si se cae del mundo muere y se borra
        if self.rect.y > HEIGHT + self.height:
            self.health = 0
            self.kill()

        #actualiza la posicion del rectangulo
        self.rect.x += dx
        self.rect.y += dy


    def shoot(self, bullet_type):
        if self.shoot_cooldown == 0 and self.ammunition > 0:
            shoot_sounds[bullet_type].play()
            self.shoot_cooldown = 20

            bullet_image = ammo_types[bullet_type]

            damage = 0

            if bullet_type == "Solo":
                damage = 20
            elif bullet_type == "Stormtrooper":
                damage = 20
            elif bullet_type == "Arachnid":
                damage = 80
            elif bullet_type == "Boss":
                damage = 10

            if self.direction == -1:
                bullet_image = pygame.transform.flip(bullet_image, True, False)
        
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.75 * self.direction),
                self.rect.centery, self.direction, bullet_image, damage)
            #Los stormtroopers no pueden hacerse daño entre si
            if bullet_type == "Stormtrooper":
                self.shoot_cooldown = 50
                bullet.can_damage_stormtrooper = False
            if bullet_type == "Arachnid":
                self.shoot_cooldown = 100
            if bullet_type == "Boss":
                self.shoot_cooldown = 5
            bullet_group.add(bullet)
            self.ammunition -= 1

            if self.direction == -1:
                self.flip = True
            else:
                self.flip = False


    def ia(self, player, world):
        inicio_vision = 0
        if self.alive and player.alive:
            if self.char_type == "Stormtrooper":
                inicio_vision = 150
            elif self.char_type == "Arachnid":
                inicio_vision = 200
                self.vision = pygame.Rect(0, 0, 300, 40)
            elif self.char_type == "Boss":
                inicio_vision = 200
                self.vision = pygame.Rect(0, 0, 350, 40)

            # Actualiza la visión de los enemigos
            self.vision.center = (self.rect.centerx + inicio_vision * self.direction, self.rect.centery)

            if self.vision.colliderect(player.rect):
                # Si el jugador está en la visión y hay munición, dispara
                if self.ammunition > 0:
                    self.update_action(3)
                    self.shoot(self.char_type)
                # Si no hay munición, intenta escapar del jugador
                elif self.rect.x < player.rect.x:
                    self.move(False, True, world)
                    self.update_action(1)
                elif self.rect.x > player.rect.x:
                    self.move(True, False, world)
                    self.update_action(1)
            else:
                # Si el jugador no esta en la vision, sigue moviendose
                if self.direction == 1:
                    ia_moving_right = True
                    ia_moving_left = False
                elif self.direction == -1:
                    ia_moving_right = False
                    ia_moving_left = True
                ia_moving_left = not ia_moving_right
                self.move(ia_moving_left, ia_moving_right, world)
                self.update_action(1)

            # Si el enemigo llega a los bordes de la pantalla, cambia de dirección
            if self.rect.x >= WIDTH - 40 or self.rect.x <= 0:
                self.direction *= -1
        #si el jugador muere o termino el nivel, los enemigos se quedan quietos
        if (not player.alive or player.level_completed) and self.alive:
            self.speed = 0
            self.ammunition = 0
            self.update_action(0)
            if player.level_completed:
                player.update_action(0)


    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #se muestra una animacion dependiendo de la accion
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    
    def update_action(self, new_action):
        #verifica que la nueva accion sea diferente de la anterior
        if new_action != self.action: 
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            if self.char_type == "Arachnid" and not self.death_sound_played:
                arachnid_death_sound.play()
                self.death_sound_played = True
            if self.char_type == "Boss" and not self.death_sound_played:
                boss_death_sound.play()
                self.death_sound_played = True
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)