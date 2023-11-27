import pygame, sqlite3, re
from config import *
from Slider import *
from Button import *
from World import *



def cambiar_musica(musica, empieza):
    playing_music = pygame.mixer.music.get_busy()  #si ya se esta reproduciendo una musica
    pygame.mixer.music.set_volume(volumen)
    if not playing_music:
        pygame.mixer.music.load(musica)
        pygame.mixer.music.play(-1, empieza)


def dibujar_fondo(backgrounds, level):
    screen.blit(backgrounds[level-1], (0,0))
    

def dibujar_HUD(hud_images, player, health_bar):
    screen.blit(hud_images[0], (5, 0))
    screen.blit(hud_images[1], (205, 10))
    screen.blit(hud_images[2], (5, HEIGHT - 40))
    screen.blit(hud_images[3], (WIDTH - 210, HEIGHT - 50))
    for x in range(player.ammunition):
        screen.blit(ammo_types["Arachnid"], (13 + (x * 10), HEIGHT - 30))
    
    health_bar.draw(player.health, 171, 30)
    draw_text(f"{player.score}", score_font, "white", 260, 15)
    draw_text(f"Time: {tiempo_restante}", score_font, "gray", WIDTH - 195, HEIGHT - 50)

    if not player.alive:
        screen.blit(lose_menu_img, (WIDTH // 2 - 350, HEIGHT // 2 + 100))
    elif show_pause_menu:
        screen.blit(pause_menu_img, (WIDTH // 2 - 350, HEIGHT // 2 - 25))
        

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_update_enemy(player):
    for stormtrooper in stormtrooper_group:
        if not show_pause_menu:
            stormtrooper.ia(player, world)
            stormtrooper.update()
        stormtrooper.draw()
    
    for arachnid in arachnid_group:
        if not show_pause_menu:
            arachnid.ia(player, world)
            arachnid.update()
        arachnid.draw()

    for boss in boss_group:
        if not show_pause_menu:
            boss.ia(player, world)
            boss.update()
        boss.draw()

def draw_update_groups(player):
    item_box_group.update(player)
    item_box_group.draw(screen)
    if not show_pause_menu and player.alive and not player.level_completed:
        bullet_group.update(player, world)
    bullet_group.draw(screen)
    lava_group.update()
    lava_group.draw(screen)
    exit_group.update()
    exit_group.draw(screen)


#MENUS
def menu_config():
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    screen.blit(settings_menu_img, (200, 280))
    # Verificar si el mouse está sobre el slider y se está presionando el botón izquierdo
    if slider.slider_left_pos < mouse_pos[0] < slider.slider_right_pos and mouse_pressed[0]:
        slider.move_slider(mouse_pos)
    volumen = slider.get_value()
    slider.render()
    screen.blit(score_table_img, (WIDTH // 2 - 10, HEIGHT // 2 + 75))
    draw_text("Music Volume", score_font, "white", WIDTH // 2 - 275, HEIGHT // 2 - 100)
    draw_text(f"{int(volumen)} %", score_font, "gray", WIDTH // 2 + 25, HEIGHT // 2 + 95)

    return volumen / 100


def menu_score(nombre_archivo):
    #crea el archivo en caso de no existir al entrar en el menu de scores
    crear_scores(nombre_archivo)
    espacios_y = 75
    screen.blit(score_menu_img, (150, 145))
    for y in range(4):
        espacios_x = 245
        espacios_y += 95
        screen.blit(score_table_img, (espacios_x, espacios_y))
        for x in range(3):
            screen.blit(score_table_img, (espacios_x, espacios_y))
            espacios_x += 175
    draw_text("LEVEL       SCORE     PLAYER", score_font, WHITE, WIDTH // 2 - 210, HEIGHT // 2 - 210)
    for nivel in range(NIVELES):
        espacios_y += 100
        nivel_score = cargar_scores(nombre_archivo, nivel+1)
        draw_text(f"NIVEL {nivel_score[0]}      {nivel_score[1]}", score_font, WHITE, espacios_x - 500, espacios_y - 275)
        draw_text(f"{nivel_score[2]}", score_font, WHITE, espacios_x - 165, espacios_y - 275)
    if retry_button.draw(screen):
        resetear_scores(nombre_archivo)


def crear_scores(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        with sqlite3.connect(nombre_archivo) as conexion:
            try:
                # Crear tabla DDL DATA DEFINITION LANGUAGE (define la estructura de los datos)
                sentencia = '''
                            create table Scores
                            (
                                nivel integer primary key autoincrement,
                                score integer,
                                player text
                            )
                            '''
                conexion.execute(sentencia)

                sentencia = '''
                            insert into Scores (score, player) values (?, ?)
                            '''

                for nivel in range(3):
                    score = 0
                    player = "Name"
                    conexion.execute(sentencia, (score, player))
            except Exception as e:
                print(f"Error al crear archivo!{e}")
        

def guardar_scores(nombre_archivo, level, score, nombre_jugador):
    #si el archivo no existe, lo crea
    crear_scores(nombre_archivo)

    with sqlite3.connect(nombre_archivo) as conexion:
        try:
            #consulta donde poner el score
            sentencia = 'SELECT score FROM Scores WHERE nivel = ?'
            
            resultado = cargar_scores(nombre_archivo, level)
            
            #verifica que el score anterior sea menor al nuevo
            if resultado[1] < score:
                sentencia = 'UPDATE Scores SET score = ?, player = ? WHERE nivel = ?'
                conexion.execute(sentencia, (score, nombre_jugador, level))


        except Exception as e:
            print(f"ERROR al guardar archivo! {e}")


def cargar_scores(nombre_archivo, level):
    resultado = ()
    with sqlite3.connect(nombre_archivo) as conexion:
        try:
            #consulta de donde sacar los valores
            sentencia = 'SELECT nivel, score, player FROM Scores WHERE nivel = ?'
            #me da una tupla con el numero del nivel, el score y el jugador de ese nivel
            resultado = conexion.execute(sentencia, (level,)).fetchone()

        except Exception as e:
            print(f"ERROR al cargar archivo! {e}")
    return resultado


def resetear_scores(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print("No existe archivo al cual limpiar scores")
    else:
        with sqlite3.connect(nombre_archivo) as conexion:
            try:
                #consulta donde poner el score
                for nivel in range(NIVELES):
                    sentencia = 'UPDATE Scores SET score = ?, player = ? WHERE nivel = ?'
                    conexion.execute(sentencia, (0, "Name", nivel + 1))


            except Exception as e:
                print(f"ERROR! {e}")


#crear botones
back_button = Button(WIDTH // 2 - 275, HEIGHT // 2 + 150, back_img, 2)
retry_button = Button(WIDTH // 2 - 75, HEIGHT // 2 + 150, retry_img, 2)
next_button = Button(WIDTH // 2 + 125, HEIGHT // 2 + 150, next_img, 2)
exit_button = Button(WIDTH // 2 + 250, HEIGHT // 2 + 250, exit_img, 2)
config_button = Button(WIDTH // 2 + 250, HEIGHT // 2 -25, config_img, 1)
score_button = Button(WIDTH // 2 + 250, HEIGHT // 2 + 50, score_img, 1)
play_button = Button(WIDTH // 2 - 250, HEIGHT // 2 + 100, play_img, 2)
level1_button = Button(WIDTH // 2 - 200, HEIGHT // 2, level1_img, 2)
level2_button = Button(WIDTH // 2 - 50, HEIGHT // 2, level2_img, 2)
level3_button = Button(WIDTH // 2 + 100, HEIGHT // 2, level3_img, 2)
#Slider para el volumen
slider = Slider((WIDTH // 2 + 75, HEIGHT // 2),
    (350, 30),
    0.2,
    0,
    100,
    on_update = lambda: volumen / 100,
    on_draw = lambda: draw_text(f"{int(volumen)} %", score_font, "gray", WIDTH // 2 + 25, HEIGHT // 2 + 95))


#se carga el jugador, su barra de vida y el mundo
player, health_bar, world = cargar_nivel(1)
#timer
pygame.time.set_timer(pygame.USEREVENT, 1000)



run = True
while run:
    clock.tick(FPS)

    if not start_game:
        cambiar_musica("Recursos//Musica//Menu.mp3", 2)
        screen.blit(menu_background, (0, 0))
        if current_menu == "main":
            screen.blit(menu_img, (150, 350))
            if score_button.draw(screen):
                current_menu = "scores"
            if config_button.draw(screen):
                current_menu = "config"
            if play_button.draw(screen):
                current_menu = "levels"
            if exit_button.draw(screen):
                run = False

        else:
            if current_menu == "scores":
                menu_score(nombre_archivo_scores)

            if current_menu == "config":
                volumen = menu_config()

            if current_menu == "levels":
                screen.blit(level_select_img, (200, 260))
                text_surface = score_font.render(player_name, True, WHITE)
                screen.blit(text_input_img, (WIDTH // 2, HEIGHT // 2 + 150))
                screen.blit(text_surface, (WIDTH // 2 + 15, HEIGHT // 2 + 165))
                if level1_button.draw(screen):
                    pygame.mixer.music.stop()
                    tiempo_restante = NORMAL_TIME
                    start_game = True
                    level = 1
                if level1_complete:
                    if level2_button.draw(screen):
                        pygame.mixer.music.stop()
                        tiempo_restante = NORMAL_TIME
                        start_game = True
                        level = 2
                    if player.level_completed:
                        level2_complete = True
                if level2_complete:
                    if level3_button.draw(screen):
                        pygame.mixer.music.stop()
                        tiempo_restante = BOSS_TIME
                        start_game = True
                        level = 3
                draw_text("Level Select", score_font, "gold", WIDTH // 2 - 90, HEIGHT // 2 - 95)
                player, health_bar, world = cargar_nivel(level)
                
            if back_button.draw(screen):
                current_menu = "main"

    else:
        #Si se termina el tiempo, el jugador pierde
        if tiempo_restante <= 0:
            player.alive = False
            player.update_action(0)
        #mostrar fondo, municion, vida y puntaje y el interfaz
        dibujar_fondo(backgrounds, level)
        #dibujar mapa del mundo
        world.draw()

        #mostrar personaje principal
        player.update()
        player.draw()

        #dibujar grupos y enemigos
        
        draw_update_groups(player)
        draw_update_enemy(player)

        #Dibujo el interfaz durante el juego
        dibujar_HUD(huds, player, health_bar)

        #verifica que el nivel se haya completado
        if level == 1:
            if player.level_completed:
                level1_complete = True
        if level == 2:
            if player.level_completed:
                level2_complete = True
        if level == 3:
            # Verificar si todas las entidades en boss_group tienen health igual a 0
            if all(boss.health == 0 for boss in boss_group):
                player.level_completed = True
        cambiar_musica(f"Recursos//Musica//Nivel{level}.mp3", 0)

        #actualizar acciones del jugador
        if player.alive and not player.level_completed and not show_pause_menu:
            if player.in_air:
                player.update_action(2) #salta
            elif mover_izq or mover_der:
                player.update_action(1) #correr
            else:
                player.update_action(0) #quieto
            if shoot and player.ammunition > 0:
                player.update_action(3) #dispara
                player.shoot("Solo")
                #deja de moverse al disparar
                mover_izq = False
                mover_der = False
            player.move(mover_izq, mover_der, world)


        if show_pause_menu or not player.alive:
            if back_button.draw(screen):
                pygame.mixer.music.stop()
                start_game = False
                show_pause_menu = False

            if retry_button.draw(screen):
                tiempo_restante = NORMAL_TIME
                if level == 3:
                    tiempo_restante = BOSS_TIME
                #carga al jugador y su barra de vida, procesa los datos del mapa del mundo
                player, health_bar, world = cargar_nivel(level)
                show_pause_menu = False

        if player.level_completed:
            screen.blit(won_menu_img, (WIDTH // 2 - 350, HEIGHT // 2 - 25))
            if level < 3 and player.alive:
                
                if next_button.draw(screen):
                    pygame.mixer.music.stop()
                    level += 1
                    tiempo_restante = NORMAL_TIME
                    if level == 3:
                        tiempo_restante = BOSS_TIME
                    player, health_bar, world = cargar_nivel(level)
                    show_pause_menu = False

            if back_button.draw(screen):
                pygame.mixer.music.stop()
                start_game = False
                show_pause_menu = False

            if retry_button.draw(screen):
                tiempo_restante = NORMAL_TIME
                if level == 3:
                    tiempo_restante = BOSS_TIME
                #carga al jugador y su barra de vida, procesa los datos del mapa del mundo
                player, health_bar, world = cargar_nivel(level)
                show_pause_menu = False
            #se guarda el score
            score = player.score + tiempo_restante
            guardar_scores(nombre_archivo_scores, level, score, player_name)
       

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #se apretan los botones
        if event.type == pygame.USEREVENT:
            if not show_pause_menu and player.alive and not player.level_completed:
                tiempo_restante -= 1
        if event.type == pygame.KEYDOWN:
            if current_menu == "levels" and not start_game:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 7:
                    # Se verifica si el caracter ingresado es una letra o numero utilizando regex
                    if re.match(r'^[a-zA-Z0-9]$', event.unicode):
                        player_name += event.unicode

            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                # Cambia el valor de show_pause_menu al presionar 
                show_pause_menu = not show_pause_menu
            if not shoot:
                if event.key == pygame.K_LEFT:
                    mover_izq = True
                if event.key == pygame.K_RIGHT:
                    mover_der = True
            if event.key == pygame.K_z:
                shoot = True
            if ((event.key == pygame.K_SPACE or event.key == pygame.K_UP)
                and player.alive and not player.in_air):
                player.jump = True
        #se sueltan los botones
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                mover_izq = False
            if event.key == pygame.K_RIGHT:
                mover_der = False
            if event.key == pygame.K_z:
                shoot = False
    
    pygame.display.update()

pygame.quit()

