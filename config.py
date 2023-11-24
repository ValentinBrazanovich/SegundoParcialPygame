import pygame
pygame.init()
clock = pygame.time.Clock()
WIDTH = 1000
HEIGHT = 800
FPS = 60

#Colores
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars: Bountyhunter")

#variables del juego
GRAVEDAD = 1
FILAS = 16
COLUMNAS = 20
TILE_SIZE = HEIGHT // FILAS
TILE_TYPES = 15 # son 6 con plataformas + (solo,storm,araña,boss) + (ammo, coin, salida, vida) + lava
AMMO_TYPES = 4
ITEM_TYPES = 3
NIVELES = 3
NORMAL_TIME = 40
BOSS_TIME = 60
nombre_archivo_scores = "Scores.db"
start_game = False
volumen = 0.2
tiempo_restante = 60
level = 1
score = 0

#fuentes
score_font = pygame.font.SysFont("Verdana", 30)

#cargar imagenes
#imagenes del menu
menu_img = pygame.image.load("Recursos\Menus\Menu.png")
menu_img = pygame.transform.scale(menu_img, (700, 375))
score_menu_img = pygame.image.load("Recursos\Menus\Window.png")
score_menu_img = pygame.transform.scale(score_menu_img, (500, 500))
settings_menu_img = pygame.image.load("Recursos\Menus\Settings table.png")
settings_menu_img = pygame.transform.scale(settings_menu_img, (600, 400))
level_select_img = pygame.image.load("Recursos\Menus\Level_select.png")
level_select_img = pygame.transform.scale(level_select_img, (600, 400))
pause_menu_img = pygame.image.load("Recursos\Menus\Pause Menu.png")
pause_menu_img = pygame.transform.scale(pause_menu_img, (200, 60))
score_table_img = pygame.image.load(r"Recursos\Menus\table.png")
score_table_img = pygame.transform.scale(score_table_img, (175, 75))
pause_menu_img = pygame.image.load("Recursos\Menus\Pause Menu.png")
pause_menu_img = pygame.transform.scale(pause_menu_img, (700, 300))
won_menu_img = pygame.image.load("Recursos\Menus\Won menu.png")
won_menu_img = pygame.transform.scale(won_menu_img, (700, 300))
lose_menu_img = pygame.transform.scale(settings_menu_img, (700, 300))
slide_bar_img = pygame.image.load("Recursos\Menus\Bar.png")
slide_bar_img = pygame.transform.scale(slide_bar_img, (350, 30))
icon_img = pygame.image.load("Recursos\halcon.ico")
pygame.display.set_icon(icon_img)

#imagenes de botones
retry_img = pygame.image.load("Recursos\Menus\BTN_Retry.png")
back_img = pygame.image.load("Recursos\Menus\home.png")
next_img = pygame.image.load("Recursos\Menus\BTN_OK.png")
exit_img = pygame.image.load("Recursos\Menus\BTN Exit.png")
config_img = pygame.image.load("Recursos\Menus\Config_btn.png")
score_img = pygame.image.load("Recursos\Menus\Score_btn.png")
play_img = pygame.image.load("Recursos\Menus\BTN PLAY.png")
back_img = pygame.image.load("Recursos\Menus\home.png")
level1_img = pygame.image.load(r"Recursos\Menus\1.png")
level2_img = pygame.image.load(r"Recursos\Menus\2.png")
level3_img = pygame.image.load(r"Recursos\Menus\3.png")

#background
backgrounds = []
for background in range(NIVELES):
    background_img = pygame.image.load(f"Recursos\Fondos\{background}.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    backgrounds.append(background_img)
menu_background = pygame.image.load(f"Recursos\Fondos\Menu.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
#HUD
health_hud = pygame.image.load("Recursos\HUD\Health_HUD.png")
health_hud = pygame.transform.scale(health_hud, (200, 60))
ammo_hud = pygame.image.load("Recursos\HUD\Ammo_HUD.png")
ammo_hud = pygame.transform.scale(ammo_hud, (520, 40))
score_hud = pygame.image.load("Recursos\HUD\Score_HUD.png")
score_hud = pygame.transform.scale(score_hud, (160, 50))
time_hud = pygame.image.load("Recursos\HUD\Time_HUD.png")
time_hud = pygame.transform.scale(time_hud, (200, 50))

huds = [health_hud,
        score_hud,
        ammo_hud, time_hud]


#sonidos
#sonidos de items
pygame.mixer.init()
coin_sound = pygame.mixer.Sound("Recursos\Items\Coin_sound.mp3")
coin_sound.set_volume(0.3)
ammo_sound = pygame.mixer.Sound("Recursos\Items\Ammo_sound.mp3")
ammo_sound.set_volume(0.5)
health_sound = pygame.mixer.Sound("Recursos\Items\Health_sound.mp3")
health_sound.set_volume(0.2)
click_sound = pygame.mixer.Sound("Recursos\Menus\click.mp3")
click_sound.set_volume(0.2)

#Sonidos de muerte
boss_death_sound = pygame.mixer.Sound("Recursos\Boss\Lego_yoda_death_sound.mp3")
boss_death_sound.set_volume(0.3)
arachnid_death_sound = pygame.mixer.Sound("Recursos\Arachnid\explode.mp3")
arachnid_death_sound.set_volume(0.3)
#Sonidos de balas
shoot_sounds = {
    "Solo"          : "",
    "Stormtrooper"  : "",
    "Arachnid"      : "",
    "Boss"          : ""
}

for shoot_sound in range(AMMO_TYPES):
    sound = pygame.mixer.Sound(f"Recursos\Projectile\{shoot_sound}.mp3")
    sound.set_volume(0.2)
    shoot_sounds["Solo" if shoot_sound == 0 else
               "Stormtrooper" if shoot_sound == 1 else
               "Arachnid" if shoot_sound == 2 else
               "Boss"] = sound

#cargar imagenes
#guarda los game tiles en una lista
img_tile_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Recursos/Plataformas/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_tile_list.append(img)

#balas
ammo_types = {
    "Solo"          : "",
    "Stormtrooper"  : "",
    "Arachnid"      : "",
    "Boss"          : ""
}
for ammo in range(AMMO_TYPES):
    img_bullet = pygame.image.load(f"Recursos/Projectile/{ammo}.png")
    ammo_types["Solo" if ammo == 0 else
               "Stormtrooper" if ammo == 1 else
               "Arachnid" if ammo == 2 else
               "Boss"] = img_bullet


#items
item_boxes = {
    "Health": "",
    "Coin"  : "",
    "Ammo"  : ""
}

for item in range(ITEM_TYPES):
    img_item = pygame.image.load(f"Recursos/Items/{item}.png")
    item_boxes["Health" if item == 0 else
               "Coin" if item == 1 else
               "Ammo"] = img_item


#sonidos
#sonidos de items
pygame.mixer.init()
coin_sound = pygame.mixer.Sound("Recursos\Items\Coin_sound.mp3")
coin_sound.set_volume(0.3)
ammo_sound = pygame.mixer.Sound("Recursos\Items\Ammo_sound.mp3")
ammo_sound.set_volume(0.5)
health_sound = pygame.mixer.Sound("Recursos\Items\Health_sound.mp3")
health_sound.set_volume(0.2)
click_sound = pygame.mixer.Sound("Recursos\Menus\click.mp3")
click_sound.set_volume(0.2)

#Sonidos de muerte
boss_death_sound = pygame.mixer.Sound("Recursos\Boss\Lego_yoda_death_sound.mp3")
boss_death_sound.set_volume(0.3)
arachnid_death_sound = pygame.mixer.Sound("Recursos\Arachnid\explode.mp3")
arachnid_death_sound.set_volume(0.3)
#Sonidos de balas
shoot_sounds = {
    "Solo"          : "",
    "Stormtrooper"  : "",
    "Arachnid"      : "",
    "Boss"          : ""
}

for shoot_sound in range(AMMO_TYPES):
    sound = pygame.mixer.Sound(f"Recursos\Projectile\{shoot_sound}.mp3")
    sound.set_volume(0.2)
    shoot_sounds["Solo" if shoot_sound == 0 else
               "Stormtrooper" if shoot_sound == 1 else
               "Arachnid" if shoot_sound == 2 else
               "Boss"] = sound


#cargar imagenes
#guarda los game tiles en una lista
img_tile_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Recursos/Plataformas/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_tile_list.append(img)


#balas
ammo_types = {
    "Solo"          : "",
    "Stormtrooper"  : "",
    "Arachnid"      : "",
    "Boss"          : ""
}
for ammo in range(AMMO_TYPES):
    img_bullet = pygame.image.load(f"Recursos/Projectile/{ammo}.png")
    ammo_types["Solo" if ammo == 0 else
               "Stormtrooper" if ammo == 1 else
               "Arachnid" if ammo == 2 else
               "Boss"] = img_bullet

#items
item_boxes = {
    "Health": "",
    "Coin"  : "",
    "Ammo"  : ""
}

for item in range(ITEM_TYPES):
    img_item = pygame.image.load(f"Recursos/Items/{item}.png")
    item_boxes["Health" if item == 0 else
               "Coin" if item == 1 else
               "Ammo"] = img_item




#Grupos
bullet_group = pygame.sprite.Group()
stormtrooper_group = pygame.sprite.Group()
arachnid_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


#variables del jugador
mover_izq = False
mover_der = False
shoot = False
current_menu = "main"
level1_complete = False
level2_complete = False
show_pause_menu = False