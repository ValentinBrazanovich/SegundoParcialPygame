from config import *
import csv
#####################
from Item import *
from Exit import *
from Entity import *
from Hazard import *
from HealthBar import *


class World():
    def __init__(self):
        self.platform_list = []

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect) #tupla
                    if tile >= 0 and tile <= 5: #plataformas
                        self.platform_list.append(tile_data)
                    elif tile == 6: #crea municion
                        item_box = Item("Ammo", x * TILE_SIZE, y * TILE_SIZE, (TILE_SIZE * 0.5, TILE_SIZE * 0.8))
                        item_box_group.add(item_box)
                    elif tile == 7: #crea una moneda
                        item_box = Item("Coin", x * TILE_SIZE, y * TILE_SIZE, (TILE_SIZE * 0.8, TILE_SIZE * 0.8))
                        item_box_group.add(item_box)
                    elif tile == 8: #crea una salida
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE, (150, 100))
                        exit_group.add(exit)
                    elif tile == 9: #crea vida/frasco de bacta
                        item_box = Item("Health", x * TILE_SIZE, y * TILE_SIZE, (TILE_SIZE * 0.8, TILE_SIZE * 0.8))
                        item_box_group.add(item_box)
                    elif tile == 10: #se crea el jugador
                        player = Entity("Solo", x * TILE_SIZE, y * TILE_SIZE, (40, 90), 5, 10, 100)
                        health_bar = HealthBar(20, 20, player.health, player.health)
                    elif tile == 11: #se crea un stormtrooper
                        stormtrooper = Entity("Stormtrooper", x * TILE_SIZE, y * TILE_SIZE, (40, 90), 2, 20, 100)
                        stormtrooper_group.add(stormtrooper)
                    elif tile == 12: #se crea una araña
                        arachnid = Entity("Arachnid", x * TILE_SIZE, y * TILE_SIZE, (90, 90), 1, 20, 200)
                        arachnid_group.add(arachnid)
                    elif tile == 13: #se crea al jefe
                        boss = Entity("Boss", x * TILE_SIZE, y * TILE_SIZE, (40, 90), 1, 8000, 450)
                        boss_group.add(boss)
                    elif tile == 14:
                        lava = Hazard(img, x * TILE_SIZE, y * TILE_SIZE)
                        lava_group.add(lava)

        return player, health_bar


    def draw(self):
        #dibuja las plataformas del nivel y otros elementos
        for tile in self.platform_list:
            screen.blit(tile[0], tile[1])

             
def reset_game():
    bullet_group.empty()
    stormtrooper_group.empty()
    arachnid_group.empty()
    item_box_group.empty()
    boss_group.empty()
    lava_group.empty()
    exit_group.empty()

    #lista vacia de tiles
    data = []
    for row in range(FILAS):
        r = [-1] * COLUMNAS
        data.append(r)

    return data

    
def cargar_nivel(level):
    try:
        world_data = reset_game()
        
        # Intenta cargar datos del nivel y crear el mundo
        with open(f'level{level}_data.csv', newline='') as levelfile:
            reader = csv.reader(levelfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        # Intenta cargar al jugador y su barra de vida, procesa los datos del mapa del mundo
        world = World()
        player, health_bar = world.process_data(world_data)

        return player, health_bar, world

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la carga del nivel y sale del programa
        print(f"Error al cargar el nivel {level}: {e}")
        pygame.quit()