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

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = load(path("Images", "Screens", "Main", image)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def hover(self, image, hover, current):
        if current == True:
            self.image = load(path("Images", "Screens", "Main", hover)).convert_alpha()
        else:
            self.image = load(path("Images", "Screens", "Main", image)).convert_alpha()

class SaveButton(MenuButton):
    def temporary(self):
        pass

class ControlsButton(MenuButton):
    def temporary(self):
        pass

class ExitButton(MenuButton):
    def temporary(self):
        pass

