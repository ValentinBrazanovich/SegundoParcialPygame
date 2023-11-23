from config import *

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False  # Se ha hecho clic y aún no se ha soltado

    def draw(self, surface):
        action = False

        # Obtener la posición del mouse
        pos = pygame.mouse.get_pos()

        # Verificar las condiciones de pasar el ratón y hacer clic
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                click_sound.play()
        else:
            # Si el ratón no está sobre el botón, restablecer el estado clicado
            self.clicked = False

        # Verificar si se ha hecho clic y soltado
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            action = True
            self.clicked = False  # Restablecer el estado clicado después de hacer clic y soltar

        # Dibujar el botón
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action