import pygame, random, time, os, sys, pyganim, threading # Python Libraries
import title, player_sprite, menu, enemy # My Libraries
from csv_convert import * # My Libraries
from pygame.locals import * # Additional
from pygame import mixer

# Initialisation
pygame.init()
mixer.init()

## -- ## Variables ## -- ##

pygame.display.set_caption("Kakureta")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

display_width = 900
display_height = 600
display = pygame.display.set_mode((display_width, display_height))

end_thread = False

FPS = 60
tilesize = 64

load = pygame.image.load
path = os.path.join

## -- ## Classes ## -- ##

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, sprite_type, surface = pygame.Surface((tilesize, tilesize))):
        super().__init__()
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == "m objects":
            self.rect = self.image.get_rect(topleft = (position[0], position[1] - tilesize))
            inflatex = -25
            inflatey = -60
        elif sprite_type == "s objects":
            self.rect = self.image.get_rect(topleft=position)
            inflatex = -15
            inflatey = -50
        elif sprite_type == "l objects":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - (tilesize * 4 - 32)))
            inflatex = -15
            inflatey = -60
        elif sprite_type == "s trees":
            self.rect = self.image.get_rect(topleft = (position[0], position[1] - tilesize))
            inflatex = -15
            inflatey = -60
        elif sprite_type == "m trees":
            self.rect = self.image.get_rect(topleft = (position[0], position[1] - tilesize * 2))
            inflatex = -60
            inflatey = -60
        elif sprite_type == "l trees":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - tilesize * 2))
            inflatex = -15
            inflatey = -60
        elif sprite_type == "s house" or sprite_type == "m house":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - tilesize * 2))
            inflatex = -15
            inflatey = -60
        elif sprite_type == "l house":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - (tilesize * 4 + 20)))
            inflatex = -15
            inflatey = -60
        elif sprite_type == "gate":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - tilesize))
            inflatey = -60
            inflatex = -20
        elif sprite_type == "shrine":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - tilesize * 2))
            inflatex = -15
            inflatey = -60
        elif sprite_type == "invisible":
            self.rect = self.image.get_rect(topleft=position)
            inflatex = -50
            inflatey = -15
        else:
            inflatex = -15
            inflatey = -20
            self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(inflatex, inflatey)

## -- ## Subroutines ## -- ##

def cursor():
    cursor_image = load(path("Images", "Screens", "Main", "cursor.png")).convert_alpha()
    cursor_image_rect = cursor_image.get_rect()
    cursor_image_rect.topleft = pygame.mouse.get_pos()
    display.blit(cursor_image, cursor_image_rect)

## -- ## Other ## -- ##

# Icons
icon = load(path("Images","heart.png"))
pygame.display.set_icon(icon)

# Title Class Objects
title_screen = title.TitleScreen()
load_button = title.LoadButton("load.png", 500, 0)
new_button = title.NewButton("new.png", -40, 100)
T_exit_button = title.ExitButton("exit.png", 0,0)
title_list = pygame.sprite.Group()
title_list.add([T_exit_button, new_button, load_button])

# Menu Class Objects
save_button = menu.SaveButton("save.png")
controls_button = menu.ControlsButton("controls.png")
exit_button = menu.ExitButton("exit.png")
menu_list = pygame.sprite.Group()
menu_list.add([save_button, controls_button, exit_button])

# Title Additional
title_hover = [1, 0, 0]
menu_hover = [1, 0 ,0]

# Player Class Objects
player = player_sprite.Player((3264,2112),"down1.png")
camera_group = player_sprite.CameraGroup()

# Visible Assets
visible_main = camera_group
visible_main.add([player])

# Collision Assets
collision_main = pygame.sprite.Group()

# Tears Group
tears = pygame.sprite.Group()

# Collected Items
tears_collected = 0

# Tear Images
tear_images = [load(path("Images", "Screens", "Level", "Tilesets", "Tears", "0.png")), load(path("Images", "Screens", "Level", "Tilesets", "Tears", "1.png"))]
tear_count = 0

# Shrines Group
shrines = pygame.sprite.Group()

# Enemy Group
enemy_group = pygame.sprite.Group()

## -- ## Map ## -- ##

def create_map():
    layouts = {
        "boundary": csv_layout("Images/Screens/Level/Data/Origin_Boundary.csv"),
        "s trees": csv_layout("Images/Screens/Level/Data/Origin_S Trees.csv"),
        "m trees": csv_layout("Images/Screens/Level/Data/Origin_M Trees.csv"),
        "l trees": csv_layout("Images/Screens/Level/Data/Origin_L Trees.csv"),
        "s objects": csv_layout("Images/Screens/Level/Data/Origin_S Objects.csv"),
        "m objects": csv_layout("Images/Screens/Level/Data/Origin_M Objects.csv"),
        "l objects": csv_layout("Images/Screens/Level/Data/Origin_L Objects.csv"),
        "s house": csv_layout("Images/Screens/Level/Data/Origin_S House.csv"),
        "m house": csv_layout("Images/Screens/Level/Data/Origin_M House.csv"),
        "l house": csv_layout("Images/Screens/Level/Data/Origin_L House.csv"),
        "hide": csv_layout("Images/Screens/Level/Data/Origin_Hide.csv"),
        "gate": csv_layout("Images/Screens/Level/Data/Origin_Gate.csv"),
        "shrine": csv_layout("Images/Screens/Level/Data/Origin_Shrine.csv"),
        "tears": csv_layout("Images/Screens/Level/Data/Origin_Spawn.csv"),
        "enemies": csv_layout("Images/Screens/Level/Data/Origin_Enemy.csv")
    }

    graphics = {
        "s trees": import_folder("Images/Screens/Level/Tilesets/s trees"),
        "m trees": import_folder("Images/Screens/Level/Tilesets/m trees"),
        "l trees": import_folder("Images/Screens/Level/Tilesets/l trees"),
        "s objects": import_folder("Images/Screens/Level/Tilesets/s objects"),
        "m objects": import_folder("Images/Screens/Level/Tilesets/m objects"),
        "l objects": import_folder("Images/Screens/Level/Tilesets/l objects"),
        "s house": import_folder("Images/Screens/Level/Tilesets/s house"),
        "m house": import_folder("Images/Screens/Level/Tilesets/m house"),
        "l house": import_folder("Images/Screens/Level/Tilesets/l house"),
        "hide": import_folder("Images/Screens/Level/Tilesets/hide"),
        "gate": import_folder("Images/Screens/Level/Tilesets/gate"),
        "shrine": import_folder("Images/Screens/Level/Tilesets/shrine"),
        "tears": import_folder("Images/Screens/Level/Tilesets/tears"),
        "enemies": import_folder("Images/Enemy")
    }

    for type, layout in layouts.items():
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                if column != "-1":
                    x = column_index * tilesize
                    y = row_index * tilesize
                    if type == "boundary":
                        tile = Tile((x, y), "invisible")
                        collision_main.add([tile])
                    if type == "s trees":
                        image = graphics["s trees"][int(column)]
                        tile = Tile((x, y), "s trees", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "m trees":
                        image = graphics["m trees"][int(column)]
                        tile = Tile((x, y), "m trees", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "l trees":
                        image = graphics["l trees"][int(column)]
                        tile = Tile((x, y), "l trees", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "s objects":
                        image = graphics["s objects"][int(column)]
                        tile = Tile((x, y), "s objects", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "m objects":
                        image = graphics["m objects"][int(column)]
                        tile = Tile((x, y), "m objects", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "l objects":
                        image = graphics["l objects"][int(column)]
                        tile = Tile((x, y), "l objects", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "s house":
                        image = graphics["s house"][int(column)]
                        tile = Tile((x, y), "s house", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "m house":
                        image = graphics["m house"][int(column)]
                        tile = Tile((x, y), "m house", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "l house":
                        image = graphics["l house"][int(column)]
                        tile = Tile((x, y), "l house", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "hide":
                        image = graphics["hide"][int(column)]
                        tile = Tile((x, y), "hide", image)
                        visible_main.add([tile])
                    if type == "gate":
                        image = graphics["gate"][int(column)]
                        tile = Tile((x, y), "gate", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "shrine":
                        image = graphics["shrine"][int(column)]
                        tile = Tile((x, y), "shrine", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                        shrines.add([tile])
                    if type == "tears":
                        image = graphics["tears"][0]
                        tile = Tile((x, y), "tears", image)
                        visible_main.add([tile])
                        tears.add([tile])
                    if type == "enemies":
                        image = graphics["enemies"][0]
                        enemytile = enemy.Enemy((x,y), image)
                        visible_main.add([enemytile])
                        enemy_group.add([enemytile])

create_map()

## -- ## Game Loops ## -- ##

# Title Loop
def title():
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            # Title Screen
            if event.type == pygame.KEYDOWN:
                global title_hover

                # Movement through buttons
                if event.key == pygame.K_DOWN:
                    selected()
                    one_index = title_hover.index(1)
                    if one_index == 2:
                        title_hover = [1, 0, 0]
                    else:
                        title_hover = [0, 0, 0]
                        title_hover[one_index + 1] = 1
                if event.key == pygame.K_UP:
                    selected()
                    one_index = title_hover.index(1)
                    if one_index == 0:
                        title_hover = [0, 0, 1]
                    else:
                        title_hover = [0, 0, 0]
                        title_hover[one_index - 1] = 1

                # Pressing enter on the right button
                if event.key == pygame.K_RETURN and title_hover[0] == 1:
                    click()
                    main()
                    #loading()
                if event.key == pygame.K_RETURN and title_hover[2] == 1:
                    click()
                    pygame.quit()
                    sys.exit()
        # Hover animation
        if title_hover[0] == 1:
            load_button.hover("load.png","loadhover.png", 200, 0, 0, 0, True)
        else:
            load_button.hover("load.png", "loadhover.png", 200, 0, -60, 0, False)
        if title_hover[1] == 1:
            new_button.hover("new.png","newhover.png", 80, 20, -40, 100, True)
        else:
            new_button.hover("new.png", "newhover.png", 80, 20, -40, 100, False)
        if title_hover[2] == 1:
            T_exit_button.hover("exit.png","exithover.png", 92, 20, 20, 200, True)
        else:
            T_exit_button.hover("exit.png", "exithover.png", 92, 20, 0, 200, False)
        title_screen.animate(display)
        title_list.draw(display)
        cursor()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

# Loading
def loading():
    global end_thread
    game_running = True
    end_thread = False

    while game_running:
        if end_thread:
            game_running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()
        display.fill([0,0,0])
        display.blit(load(path("Images", "Screens", "Main", "loading.png")), (0, 0))
        time.sleep(2) # Temporary
        pygame.display.flip()
        clock.tick(FPS)

# Main Loop
def main():
    loading_screen = threading.Thread(target= loading, args=(), daemon=True)
    loading_screen.start()
    game_running = True
    inventory = False
    controls = False
    game_over = False
    while game_running:
        global tears_collected
        global tear_count
        global tear_images
        global end_thread
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                global menu_hover
                if event.key == pygame.K_e:
                    inventory = not inventory
                    controls = False
                    menu_hover = [1, 0, 0]
                # Movement through buttons
                if event.key == pygame.K_DOWN and inventory:
                    selected()
                    one_index = menu_hover.index(1)
                    if one_index == 2:
                        menu_hover = [1, 0, 0]
                    else:
                        menu_hover = [0, 0, 0]
                        menu_hover[one_index + 1] = 1
                if event.key == pygame.K_UP and inventory:
                    selected()
                    one_index = menu_hover.index(1)
                    if one_index == 0:
                        menu_hover = [0, 0, 1]
                    else:
                        menu_hover = [0, 0, 0]
                        menu_hover[one_index - 1] = 1
                if event.key == pygame.K_RETURN and inventory and menu_hover == [0, 0, 1]:
                    click()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN and inventory and menu_hover == [0, 1, 0]:
                    click()
                    controls = True
        title_music = False
        if title_music == False:
            mixer.music.fadeout(60)
            mixer.music.unload()
        main_music = True
        if main_music == True:
            background_music()
        end_thread = True
        loading_screen.join()
        display.fill([91, 161, 204])
        visible_main.custom_draw(display, player)
        display.fill((87, 59, 227), special_flags=pygame.BLEND_MULT)

        player_rect = player.hitbox.copy()
        keypress = pygame.key.get_pressed()

        if inventory == True:
            if controls == True:
                display.blit(load(path("Images","Screens","Main","controlsmenu.png")), (0, 0))
            else:
                display.blit(load(path("Images", "Screens", "Main", "pause.png")), (0, 0))
                font = pygame.font.SysFont(None, 64)
                tears_text = font.render(str(tears_collected), True, [0,0,0])
                display.blit(tears_text, (480,178))
                if menu_hover[0] == 1:
                    save_button.hover("save.png", "savehover.png",  True)
                else:
                    save_button.hover("save.png", "savehover.png", False)
                if menu_hover[1] == 1:
                    controls_button.hover("controls.png", "controlshover.png", True)
                else:
                    controls_button.hover("controls.png", "controlshover.png", False)
                if menu_hover[2] == 1:
                    exit_button.hover("exit.png", "exithover.png", True)
                else:
                    exit_button.hover("exit.png", "exithover.png", False)
                menu_list.draw(display)
        elif game_over:
            pygame.draw.rect(display, [0, 0, 0], pygame.Rect(100, 100, 700, 400))
            game_font = pygame.font.SysFont(None, 80)
            game_text = game_font.render("GAME OVER", True, [152,2,30])
            display.blit(game_text, (275,200))
            if keypress[K_ESCAPE]:
                pygame.quit()
                sys.exit()
        else:
            player.move(keypress)
            for slime in enemy_group:
                slime.move(collision_main, player)
                if slime.move(collision_main, player) == True:
                    game_over = True
            display.blit(load(path("Images", "Screens", "Main", "HUD.png")), (0, 0))
            display.blit(load(path("Images", "Screens", "Main", "notseen.png")), (0, 0))

            # Collision
            for sprite in collision_main:
                if sprite.hitbox.colliderect(player.hitbox):
                    player.hitbox = player_rect

            # Counter reset for tear animation
            if tear_count < 100:
                tear_count += 1
            else:
                tear_count = 0

            # Tear Collision
            for tear in tears:
                tear.image = tear_images[(tear_count // 16) % len(tear_images)]
                if tear.hitbox.colliderect(player.hitbox):
                    tear.kill()
                    tear_get()
                    tears_collected += 1

            # Shrine Purify
            for shrine in shrines:
                if keypress[K_i] and shrine.rect.colliderect(player.hitbox) and tears_collected >= 1:
                    shrines.remove([shrine])
                    shrine.image = load(path("Images", "Screens", "Level", "Tilesets", "Shrine", "1.png"))
                    shrine_pure()
                    tears_collected -= 1

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

## -- ## Sound ## -- ##

pygame.mixer.set_num_channels(8)

# Title Screen Music
title_music = True
if title_music == True:
    mixer.music.load("Music/Menu.mp3")
    mixer.music.set_volume(0.4)
    mixer.music.play(-1)

# Main Game Music
main_channel = pygame.mixer.Channel(6)
main_music = False
main_sound = mixer.Sound("Music/Main.mp3")
def background_music():
    if not main_channel.get_busy():
        mixer.Sound.play(main_sound)

# Title Select Sound
select_sound = mixer.Sound("Music/MenuSelect.mp3")
def selected():
    mixer.Sound.play(select_sound)

# Enter Sound
enter_sound = mixer.Sound("Music/Click.mp3")
def click():
    mixer.Sound.play(enter_sound)

# Tear Pickup Sound
tear_sound = mixer.Sound("Music/Tear.wav")
def tear_get():
    mixer.Sound.play(tear_sound)

# Shrine Sound
shrine_sound = mixer.Sound("Music/Woosh.mp3")
def shrine_pure():
    mixer.Sound.play(shrine_sound)

## -- ## Main ## -- ##

title()
