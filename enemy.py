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
tilesize = 64

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, surface = pygame.Surface((tilesize, tilesize))):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-10, -10)
        self.movement = 4

    def move(self, group, player):
        enemy_rect = self.hitbox.copy()
        self.hitbox.move_ip(0, self.movement)
        self.rect.center = self.hitbox.center
        for sprite in group:
            if sprite.hitbox.colliderect(self.hitbox):
                self.hitbox = enemy_rect
                self.movement = -self.movement
        if self.hitbox.colliderect(player.hitbox):
            return True
