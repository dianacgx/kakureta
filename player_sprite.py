import pygame, random, time, os, sys, pyganim
from pygame.locals import *
from pygame import mixer

pygame.init()

display_width = 900
display_height = 600
display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
load = pygame.image.load
path = os.path.join

FPS = 60

# Walk Animation
walk_up = [load(path("Images", "Player", "Movement", "up1.png")), load(path("Images", "Player", "Movement", "up2.png")),
          load(path("Images", "Player", "Movement", "up3.png")), load(path("Images", "Player", "Movement", "up4.png")),
          load(path("Images", "Player", "Movement", "up5.png")), load(path("Images", "Player", "Movement", "up6.png")),
          load(path("Images", "Player", "Movement", "up7.png"))]
walk_down = [load(path("Images", "Player", "Movement", "down1.png")), load(path("Images", "Player", "Movement", "down2.png")),
            load(path("Images", "Player", "Movement", "down3.png")), load(path("Images", "Player", "Movement", "down4.png")),
            load(path("Images", "Player", "Movement", "down5.png")), load(path("Images", "Player", "Movement", "down6.png")),
            load(path("Images", "Player", "Movement", "down7.png"))]
walk_left = [load(path("Images", "Player", "Movement", "left1.png")), load(path("Images", "Player", "Movement", "left2.png")),
            load(path("Images", "Player", "Movement", "left3.png")), load(path("Images", "Player", "Movement", "left4.png")),
            load(path("Images", "Player", "Movement", "left5.png")), load(path("Images", "Player", "Movement", "left6.png")),
            load(path("Images", "Player", "Movement", "left7.png"))]
walk_right = [load(path("Images", "Player", "Movement", "right1.png")), load(path("Images", "Player", "Movement", "right2.png")),
            load(path("Images", "Player", "Movement", "right3.png")), load(path("Images", "Player", "Movement", "right4.png")),
            load(path("Images", "Player", "Movement", "right5.png")), load(path("Images", "Player", "Movement", "right6.png")),
            load(path("Images", "Player", "Movement", "right7.png"))]

crouch_up = [load(path("Images", "Player", "Crouch", "up1.png")), load(path("Images", "Player", "Crouch", "up2.png")),
          load(path("Images", "Player", "Crouch", "up3.png")), load(path("Images", "Player", "Crouch", "up4.png")),
          load(path("Images", "Player", "Crouch", "up5.png")), load(path("Images", "Player", "Crouch", "up6.png")),
          load(path("Images", "Player", "Crouch", "up7.png"))]
crouch_down = [load(path("Images", "Player", "Crouch", "down1.png")), load(path("Images", "Player", "Crouch", "down2.png")),
            load(path("Images", "Player", "Crouch", "down3.png")), load(path("Images", "Player", "Crouch", "down4.png")),
            load(path("Images", "Player", "Crouch", "down5.png")), load(path("Images", "Player", "Crouch", "down6.png")),
            load(path("Images", "Player", "Crouch", "down7.png"))]
crouch_left = [load(path("Images", "Player", "Crouch", "left1.png")), load(path("Images", "Player", "Crouch", "left2.png")),
            load(path("Images", "Player", "Crouch", "left3.png")), load(path("Images", "Player", "Crouch", "left4.png")),
            load(path("Images", "Player", "Crouch", "left5.png")), load(path("Images", "Player", "Crouch", "left6.png")),
            load(path("Images", "Player", "Crouch", "left7.png"))]
crouch_right = [load(path("Images", "Player", "Crouch", "right1.png")), load(path("Images", "Player", "Crouch", "right2.png")),
            load(path("Images", "Player", "Crouch", "right3.png")), load(path("Images", "Player", "Crouch", "right4.png")),
            load(path("Images", "Player", "Crouch", "right5.png")), load(path("Images", "Player", "Crouch", "right6.png")),
            load(path("Images", "Player", "Crouch", "right7.png"))]

image_count = len(walk_up)
frame_count = 7
walk_count = 0
sprint_max = 100
can_sprint = True
crouching = False
sprint_colour = [75, 174, 246]

class Player(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__()
        self.image = load(path("Images", "Player", "Movement", image)).convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-8, -40)
        self.last = ""

    def move(self, keypress):
        global walk_count
        global frame_count
        global sprint_max
        global can_sprint
        global sprint_colour
        global crouching

        x = 6
        y = 6

        pygame.draw.rect(display, sprint_colour, pygame.Rect(40, 25, (3 * sprint_max), 35))

        if crouching == False:
            if keypress[K_LSHIFT] and sprint_max > 0 and can_sprint == True:
                x = 8
                y = 8
                frame_count = 5
                sprint_max -= 1
            else:
                if sprint_max != 100:
                    if sprint_max == 0:
                        can_sprint = False
                        sprint_colour = [100, 100, 100]
                    sprint_max += 0.25
                    if sprint_max == 100:
                        can_sprint = True
                        sprint_colour = [75, 174, 246]
                frame_count = 7
        elif crouching == True:
            x = 3
            y = 3
            frame_count = 16
            if sprint_max != 100:
                if sprint_max == 0:
                    can_sprint = False
                    sprint_colour = [100, 100, 100]
                sprint_max += 0.25
                if sprint_max == 100:
                    can_sprint = True
                    sprint_colour = [75, 174, 246]

            # Reset walk_count if it is too large
        if walk_count >= image_count * frame_count:
            walk_count = 0

        # Movement
        if keypress[K_RIGHT] or keypress[K_d]:
            self.hitbox.move_ip(x, 0)
            if keypress[K_LCTRL]:
                self.image = crouch_right[(walk_count // frame_count) % len(crouch_right)]
                crouching = True
            else:
                self.image = walk_right[(walk_count // frame_count) % len(walk_right)]
                crouching = False
            walk_count += 1
            self.last = "right"
        elif keypress[K_LEFT] or keypress[K_a]:
            self.hitbox.move_ip(-x, 0)
            if keypress[K_LCTRL]:
                self.image = crouch_left[(walk_count // frame_count) % len(crouch_left)]
                crouching = True
            else:
                self.image = walk_left[(walk_count // frame_count) % len(walk_left)]
                crouching = False
            walk_count += 1
            self.last = "left"
        elif keypress[K_UP] or keypress[K_w]:
            self.hitbox.move_ip(0, -y)
            if keypress[K_LCTRL]:
                self.image = crouch_up[(walk_count // frame_count) % len(crouch_up)]
                crouching = True
            else:
                self.image = walk_up[(walk_count // frame_count) % len(walk_up)]
                crouching = False
            walk_count += 1
            self.last = "up"
        elif keypress[K_DOWN] or keypress[K_s]:
            self.hitbox.move_ip(0, y)
            if keypress[K_LCTRL]:
                self.image = crouch_down[(walk_count // frame_count) % len(crouch_down)]
                crouching = True
            else:
                self.image = walk_down[(walk_count // frame_count) % len(walk_down)]
                crouching = False
            walk_count += 1
            self.last = "down"
        # Keeps the first frame active when idle
        elif self.last != "":
            if self.last == "up":
                if keypress[K_LCTRL]:
                    self.image = crouch_up[0]
                else:
                    self.image = walk_up[0]
            elif self.last == "down":
                if keypress[K_LCTRL]:
                    self.image = crouch_down[0]
                else:
                    self.image = walk_down[0]
            elif self.last == "left":
                if keypress[K_LCTRL]:
                    self.image = crouch_left[0]
                else:
                    self.image = walk_left[0]
            elif self.last == "right":
                if keypress[K_LCTRL]:
                    self.image = crouch_right[0]
                else:
                    self.image = walk_right[0]
        # Reset the walk_count when idle
        else:
            walk_count = 0
        self.rect.center = self.hitbox.center

    def check_move(self, keypress):
        if keypress[K_LEFT] or keypress[K_RIGHT] or keypress[K_UP] or keypress[K_DOWN]:
            return True

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor = load(path("Images", "Screens", "Level", "Tilesets", "tilemap", "Origin.png")).convert()
        self.floor_rectangle = self.floor.get_rect(topleft = (0, 0))

    def custom_draw(self, display, player):
        self.offset.x = player.rect.centerx - (display_width // 2)
        self.offset.y = player.rect.centery - (display_height // 2)

        floor_offset = self.floor_rectangle.topleft - self.offset
        display.blit(self.floor, floor_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            display.blit(sprite.image, offset_position)


def walking(right):
    walk = pygame.mixer.Channel(2)
    walk_sound = mixer.Sound("Music/Walking.mp3")
    if walk.get_busy() == False:
        # Don't play anything
        walk.play(walk_sound)
    if right == False:
        walk.stop()