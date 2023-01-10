import pygame, random, time, os, sys, pyganim
from pygame.locals import *

pygame.init()

display_width = 900
display_height = 600
display = pygame.display.set_mode((display_width, display_height))
load = pygame.image.load
path = os.path.join

tilesize = 64

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, surface = None):
        super().__init__()
        if surface is None:
            self.image = pygame.Surface((tilesize, tilesize))
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-128, -128)
        self.collidebox = self.rect.inflate(64, 64)
        self.movement = 3
        self.move_up = [load(path("Images", "Enemy", "1.png")), load(path("Images", "Enemy", "11.png"))]
        self.move_down = [load(path("Images", "Enemy", "0.png")), load(path("Images", "Enemy", "01.png"))]
        self.walk_count = 0
        self.frame_count = 20

    def move(self, group, player):
        enemy_rect = self.hitbox.copy()
        if self.walk_count >= len(self.move_up) * self.frame_count:
            self.walk_count = 0
        if self.movement == 3:
            self.image = self.move_down[(self.walk_count // self.frame_count) % len(self.move_down)]
            self.walk_count += 1
        elif self.movement == -3:
            self.image = self.move_up[(self.walk_count // self.frame_count) % len(self.move_up)]
            self.walk_count += 1
        self.hitbox.move_ip(0, self.movement)
        self.rect.center = self.hitbox.center
        self.collidebox.center = self.hitbox.center
        for sprite in group:
            if sprite.hitbox.colliderect(self.hitbox):
                self.hitbox = enemy_rect
                self.movement = -self.movement
        if self.collidebox.colliderect(player.hitbox):
            return True


class Fighter(pygame.sprite.Sprite):
    def __init__(self, position, surface = pygame.Surface((tilesize, tilesize))):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-5, -5)
        self.spx = 2.5
        self.spy = 2.5
        self.original_position = position

    def move(self, group, player, seen):
        if seen:
            self.image = load(path("Images", "Fighter", "1.png"))
            if player.rect.x > self.rect.x:
                self.spx = 2.5
            elif player.rect.x < self.rect.x:
                self.spx = -2.5
            if player.rect.y > self.rect.y:
                self.spy = 2.5
            elif player.rect.y < self.rect.y:
                self.spy = -2.5
            self.hitbox.move_ip(self.spx, self.spy)
            self.rect.center = self.hitbox.center
            if self.hitbox.colliderect(player.hitbox):
                return True
        else:
            self.image = load(path("Images", "Fighter", "0.png"))
            self.rect.x, self.rect.y = self.original_position
            self.hitbox.x, self.hitbox.y = self.original_position



