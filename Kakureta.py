import pygame, random, time, os, sys, pyganim, threading, json # Python Libraries
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

## -- ## Game Save Data ## -- ##

data = {
    "tears_collected": 0,
    "tears_left": [],
    "purified_shrines": 0,
    "shrines_left": [],
    "player_position": (3264, 2112),
    "enemy_positions": [],
    "fighter_positions": [],
    "spotted": False,
    "text_crawl": True,
    "first_tear": True
}

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
        self.base_x = self.rect.x

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
camera_group = player_sprite.CameraGroup()

# Visible Assets
visible_main = camera_group

# Collision Assets
collision_main = pygame.sprite.Group()

# Tears Group
tears = pygame.sprite.Group()

# Shrines Group
shrines = pygame.sprite.Group()

# Enemy Group
enemy_group = pygame.sprite.Group()
fighter_group = pygame.sprite.Group()

# Extras
game_sound_available = True
sign = pygame.sprite.Group()
hideables = pygame.sprite.Group()

## -- ## Map ## -- ##

def create_map(new_game, data):
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
        "enemies": csv_layout("Images/Screens/Level/Data/Origin_Enemy.csv"),
        "fighters": csv_layout("Images/Screens/Level/Data/Origin_Fighter.csv")
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
        "enemies": import_folder("Images/Enemy"),
        "fighters": import_folder("Images/Fighter")
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
                        if column == "8":
                            sign.add([tile])
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
                        hideables.add([tile])
                    if type == "gate":
                        image = graphics["gate"][int(column)]
                        tile = Tile((x, y), "gate", image)
                        visible_main.add([tile])
                        collision_main.add([tile])
                    if type == "shrine":
                        image = graphics["shrine"][int(column)]
                        if new_game:
                            tile = Tile((x, y), "shrine", image)
                            visible_main.add([tile])
                            collision_main.add([tile])
                            shrines.add([tile])
                        else:
                            shrines_left = data["shrines_left"]
                            if [x, y] in shrines_left:
                                tile = Tile((x, y), "shrine", image)
                                visible_main.add([tile])
                                collision_main.add([tile])
                                shrines.add([tile])
                            else:
                                image = graphics["shrine"][1]
                                tile = Tile((x, y), "shrine", image)
                                visible_main.add([tile])
                                collision_main.add([tile])
                    if type == "tears":
                        image = graphics["tears"][0]
                        if new_game:
                            tile = Tile((x, y), "tears", image)
                            visible_main.add([tile])
                            tears.add([tile])
                        else:
                            tears_left = data["tears_left"]
                            if [x, y] in tears_left:
                                tile = Tile((x, y), "tears", image)
                                visible_main.add([tile])
                                tears.add([tile])
                    if type == "enemies":
                        image = graphics["enemies"][0]
                        if new_game:
                            enemytile = enemy.Enemy((x, y), image)
                            visible_main.add([enemytile])
                            enemy_group.add([enemytile])
                        else:
                            enemy_position = data["enemy_positions"]
                            enemytile = enemy.Enemy((x, y), image)
                            visible_main.add([enemytile])
                            enemy_group.add([enemytile])
                    if type == "fighters":
                        image = graphics["fighters"][0]
                        if new_game:
                            fightertile = enemy.Fighter((x, y), image)
                            visible_main.add([fightertile])
                            fighter_group.add([fightertile])
                            collision_main.add([fightertile])
    if not new_game:
        fighter_position = data["fighter_positions"]
        image = graphics["fighters"][0]
        for i in range(0, len(fighter_position)):
            x = fighter_position[i][0]
            y = fighter_position[i][1]
            fightertile = enemy.Fighter((x, y), image)
            visible_main.add([fightertile])
            fighter_group.add([fightertile])
            collision_main.add([fightertile])

## -- ## Game Loops ## -- ##

# Title Loop
def title():
    global data
    global player
    global visible_main
    game_running = True
    nosaves = False
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
                if event.key == pygame.K_RETURN and title_hover[0] == 1: # Load
                    try:
                        with open("game_data.txt") as save_file:
                            data = json.load(save_file)
                        click()
                        create_map(False, data)
                        player = player_sprite.Player(data["player_position"], "down1.png")
                        visible_main.add([player])
                        main()
                    except:
                        nosaves = True
                        savetimer = 0
                if event.key == pygame.K_RETURN and title_hover[1] == 1: # New
                    click()
                    create_map(True, data)
                    player = player_sprite.Player(data["player_position"], "down1.png")
                    visible_main.add([player])
                    main()
                if event.key == pygame.K_RETURN and title_hover[2] == 1: # Exit
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
        try:
            if savetimer <= 60:
                savetimer += 1
        except:
            pass
        if nosaves and savetimer <= 60:
            display.blit(load(path("Images", "Screens", "Title", "nosaves.png")), (0, display_height - 100))
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
    gamesaved = False
    text_crawl = data["text_crawl"]
    seen = data["spotted"]
    crouching = False
    game_over = False
    first_tear = data["first_tear"]
    collide_tear = False
    shrine_count = 0
    next_sequence_2 = False
    tear_images = [load(path("Images", "Screens", "Level", "Tilesets", "Tears", "0.png")),
                   load(path("Images", "Screens", "Level", "Tilesets", "Tears", "1.png"))]
    tear_count = 0
    sequence = 0
    hide_timer = 0
    starting_options = ["What happened?", "Where did everyone go?", "I should try talking to that wisp..."]
    s_num = 0
    starting_text_1 = starting_options[s_num]
    text_iterator = iter(starting_text_1)
    display_text = ""
    tsuki_options1 = [load(path("Images", "Dialogue", "tsuki_head.png")), load(path("Images", "Dialogue", "tsuki_think.png")),
                      load(path("Images", "Dialogue", "tsuki_thinkhard.png"))]
    t_num = 0
    starting_options_2 = ["Hello?", "Tsuki... please help us.", "Himari? What happened?", "The island...",
                        "It was overrun by Yokai.", "All of us got killed.", "How do I help?!", "Deposit our souls and tears.",
                        "Put us in the shrines.", "Please don't get caught by them.", "I'll try.", "Thank you, Himari."]
    s2_num = 0
    starting_text_2 = starting_options_2[s2_num]
    text_iterator_2 = iter(starting_text_2)
    tsuki_options2 = [load(path("Images", "Dialogue", "tsuki_head.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tsuki_think.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tsuki_shocked.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tear.png")),
                      load(path("Images", "Dialogue", "tsuki_think.png")),
                      load(path("Images", "Dialogue", "tsuki_thank.png"))]
    t2_num = 0
    display_text_2 = ""
    shrine_images = [load(path("Images", "Shrine_Animation", "0.png")), load(path("Images", "Shrine_Animation", "1.png"))]
    game_over_image = load(path("Images", "Screens", "Main", "gameover.png"))
    game_over_surface = pygame.Surface(game_over_image.get_rect().size)
    game_over_surface.set_colorkey((1, 1, 1))
    game_over_surface.fill((1, 1, 1))
    game_over_surface.blit(game_over_image, (0, 0))
    alpha = 0

    while game_running:
        global end_thread
        global game_sound_available
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
                if event.key == pygame.K_RETURN and inventory and menu_hover == [1, 0, 0]:
                    click()
                    save_tear = []
                    for tear in tears:
                        save_tear.append((tear.rect.x, tear.rect.y))
                    data["tears_left"] = save_tear
                    save_shrine = []
                    for shrine in shrines:
                        save_shrine.append((shrine.rect.x, shrine.rect.y))
                    save_enemies = []
                    for enemies in enemy_group:
                        save_enemies.append((enemies.rect.x, enemies.rect.y))
                    save_fighters = []
                    for fighters in fighter_group:
                        save_fighters.append((fighters.rect.x, fighters.rect.y))
                    spotted = seen
                    data["shrines_left"] = save_shrine
                    data["enemy_positions"] = save_enemies
                    data["fighter_positions"] = save_fighters
                    data["spotted"] = spotted
                    data["text_crawl"] = text_crawl
                    data["first_tear"] = first_tear
                    data["player_position"] = (player.rect.x, player.rect.y)
                    with open("game_data.txt", "w") as save_file:
                        json.dump(data, save_file)
                    gamesaved = True
                    savetimer = 0
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

        if inventory and not game_over:
            if controls == True:
                display.blit(load(path("Images","Screens","Main","controlsmenu.png")), (0, 0))
            else:
                display.blit(load(path("Images", "Screens", "Main", "pause.png")), (0, 0))
                font = pygame.font.SysFont(None, 64)
                tears_text = font.render(str(data["tears_collected"]), True, [0,0,0])
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
                try:
                    if savetimer <= 60:
                        savetimer += 1
                except:
                    pass
                if gamesaved and savetimer <= 60:
                    display.blit(load(path("Images", "Screens", "Title", "gamesaved.png")), (0, display_height - 100))
        elif game_over:
            if game_sound_available:
                game_over_sound()
                game_sound_available = False
            alpha = alpha + 5
            game_over_surface.set_alpha(alpha)
            display.blit(game_over_surface, (0, 0))
            if keypress[K_ESCAPE]:
                pygame.quit()
                sys.exit()
        else:
            for fighter in fighter_group:
                fighter.move(collision_main, player, seen)
                if fighter.move(collision_main, player, seen) == True:
                    game_over = True
            if seen:
                display.blit(load(path("Images", "Screens", "Main", "seen.png")), (0, 0))
                display.blit(load(path("Images", "enemyeffect.png")), (0, 0))
            else:
                display.blit(load(path("Images", "Screens", "Main", "notseen.png")), (0, 0))
            if text_crawl:
                display.blit(load(path("Images", "Dialogue", "tsuki.png")), (50, 400))
                display.blit(tsuki_options1[t_num], (650, 300))
                if len(display_text) < len(starting_text_1):
                    display_text += next(text_iterator)
                if len(display_text) == len(starting_text_1):
                    next_sequence = True
                font = pygame.font.SysFont("Consolas", 28)
                start_text = font.render(display_text, True, [255, 255, 255])
                font2 = pygame.font.SysFont("Consolas", 20)
                press_text = font2.render("Press X", True, [255, 255, 255])
                display.blit(start_text, (100, 470))
                display.blit(press_text, (575, 550))
            if keypress[K_x] and text_crawl and next_sequence:
                s_num += 1
                t_num += 1
                if s_num == len(starting_options):
                    text_crawl = False
                    first_tear = True
                else:
                    starting_text_1 = starting_options[s_num]
                    text_iterator = iter(starting_text_1)
                    display_text = ""
                    next_sequence = False
            for tear in tears:
                if tear.hitbox.colliderect(player.hitbox):
                    collide_tear = True
            if first_tear and collide_tear:
                display.blit(load(path("Images", "Dialogue", "tsuki.png")), (50, 400))
                display.blit(tsuki_options2[t2_num], (650, 300))
                if len(display_text_2) < len(starting_text_2):
                    display_text_2 += next(text_iterator_2)
                if len(display_text_2) == len(starting_text_2):
                    next_sequence_2 = True
                font = pygame.font.SysFont("Consolas", 28)
                start_text = font.render(display_text_2, True, [255, 255, 255])
                font2 = pygame.font.SysFont("Consolas", 20)
                press_text = font2.render("Press X", True, [255, 255, 255])
                display.blit(start_text, (100, 470))
                display.blit(press_text, (575, 550))
            if keypress[K_x] and first_tear and next_sequence_2 and collide_tear:
                s2_num += 1
                t2_num += 1
                if s2_num == len(starting_options_2):
                    first_tear = False
                else:
                    starting_text_2 = starting_options_2[s2_num]
                    text_iterator_2 = iter(starting_text_2)
                    display_text_2 = ""
                    next_sequence_2 = False
            player.move(keypress)
            for slime in enemy_group:
                slime.move(collision_main, player)
                if slime.move(collision_main, player) == True:
                    seen = True
            display.blit(load(path("Images", "Screens", "Main", "HUD.png")), (0, 0))

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
                if not first_tear:
                    if tear.hitbox.colliderect(player.hitbox):
                        tear.kill()
                        tear_get()
                        data["tears_collected"] += 1

            # Shrine Purify
            for shrine in shrines:
                if keypress[K_i] and shrine.rect.colliderect(player.hitbox) and data["tears_collected"] >= 1:
                    shrines.remove([shrine])
                    shrine.image = load(path("Images", "Screens", "Level", "Tilesets", "Shrine", "1.png"))
                    shrine_pure()
                    data["tears_collected"] -= 1
                    data["purified_shrines"] += 1
                elif shrine.rect.colliderect(player.hitbox):
                    if shrine_count < 100:
                        shrine_count += 1
                    else:
                        shrine_count = 0
                    shrine.image = shrine_images[(tear_count // 16) % len(tear_images)]
                else:
                    shrine.image = load(path("Images", "Screens", "Level", "Tilesets", "Shrine", "0.png"))

            # Display Sign
            for message in sign:
                if message.rect.colliderect(player.hitbox):
                    display.blit(load(path("Images", "Screens", "Main", "sign.png")), (0, display_height - 300))

            # Grass Rustling Animation
            shake = 5
            for grass in hideables:
                max_left = grass.base_x - 10
                max_right = grass.base_x + 10
                if grass.rect.colliderect(player.hitbox) and player.check_move(keypress):
                        if grass.rect.x > max_left or grass.rect.x < max_right:
                            grass.rect.x = grass.base_x
                        grass.rect.x += shake
                        shake = -shake
                        bush_effect()
                else:
                    grass.rect.x = grass.base_x
                if grass.rect.colliderect(player.hitbox):
                    if hide_timer < 360:
                        hide_timer += 1
                    else:
                        hide_timer = 0
                    if keypress[K_LCTRL]:
                        crouching = True
                    else:
                        crouching = False
                    if hide_timer >= 300 and crouching:
                        seen = False
                    elif hide_timer >= 350:
                        seen = False
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

# Game Over Sound
over_sound = mixer.Sound("Music/GameOver.mp3")
def game_over_sound():
    mixer.Sound.play(over_sound)

# Bush Rustling Sound
bush_sound = mixer.Sound("Music/Bush.mp3")
def bush_effect():
    mixer.Sound.play(bush_sound)

## -- ## Main ## -- ##

title()
