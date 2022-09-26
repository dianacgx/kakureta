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

screen_frames = 300

screen_cycle = pyganim.PygAnimation([(load(path("Images", "Screens", "Title", "titlescreendark.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark2.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark3.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark4.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark5.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark6.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark7.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark8.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark9.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark10.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark11.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark12.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark13.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark14.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark15.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark16.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark17.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark18.png")), screen_frames),
                                     (load(path("Images", "Screens", "Title", "titlescreendark19.png")), screen_frames), (load(path("Images", "Screens", "Title", "titlescreendark20.png")), screen_frames)])
screen_cycle.play()

class TitleButton(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = load(path("Images", "Screens", "Title", image)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 130 + x
        self.rect.y = 250 + y
        
    def hover(self, image, hover, x, y, x1, y1, current):
        if current == True:
            self.image = load(path("Images", "Screens", "Title", hover)).convert_alpha()
            divx = x / 2
            divy = y / 2
            self.rect.x = (130 + x1) - divx
            self.rect.y = (250 + y1) - divy
        else:
            self.image = load(path("Images", "Screens", "Title", image)).convert_alpha()
            self.rect.x = 130 + x1
            self.rect.y = 250 + y1

class ExitButton(TitleButton):
    def temporary(self):
        return True

class NewButton(TitleButton):
    def temporary(self):
        return True

class LoadButton(TitleButton):
    def temporary(self):
        return True

class TitleScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load(path("Images", "Screens", "Title", "titlescreendark.png"))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def animate(self, display):
        screen_cycle.blit(display, (self.rect.x, self.rect.y))

