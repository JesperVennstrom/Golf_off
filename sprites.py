import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.player_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.radius = TILESIZE // 2
        
        self.index = 0

        self.hits = False
        self.game.first_hit = False
        self.counter = 1

        self.hit_side = False
        self.hit_top = False

        self.first_time = True

        self.speed = 0
        self.pos_start = (0, 0)
        self.pos_end = (0, 0)

        self.x = x * TILESIZE

        self.y = y * TILESIZE

        self.angle = 0

        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide()
        self.movement()
        

    def collide(self):
        block_rect = self.game.block_list[0].unionall(self.game.block_list)
        self.game.players[self.index-1].hits = block_rect.contains(self.game.players[self.index-1].rect)

        if not self.game.players[self.index-1].hits and not self.game.first_hit:
            self.game.first_hit = True
            self.game.players[self.index-1].hit_side = False
            self.game.players[self.index-1].hit_top = False
            self.game.players[self.index-1].counter = 0
            self.game.players[self.index-1].current = self.game.players[self.index-1].rect.copy()

        if self.game.first_hit:
            if self.game.players[self.index-1].hits and self.game.players[self.index-1].counter == 1:
                self.game.players[self.index-1].hit_side = True
            if self.game.players[self.index-1].hits and self.game.players[self.index-1].counter == 2:
                self.game.players[self.index-1].hit_top = True

            if self.game.players[self.index-1].counter == 2:
                self.game.players[self.index-1].counter += 1
                self.game.players[self.index-1].rect.x = self.game.players[self.index-1].copy.x

            if self.game.players[self.index-1].counter == 1:
                self.game.players[self.index-1].counter += 1
                self.game.players[self.index-1].rect.y = self.copy.y
                self.game.players[self.index-1].rect.x = self.game.players[self.index-1].current.x

            if self.game.players[self.index-1].counter == 0:
                self.game.players[self.index-1].counter += 1
                self.game.players[self.index-1].rect.x = self.game.players[self.index-1].copy.x

            if self.game.players[self.index-1].hit_side and self.game.players[self.index-1].hit_top  and self.game.players[self.index-1].counter == 3:
                print("corner")
                self.game.first_hit = False
                self.game.players[self.index-1].angle = 180 * 0.0174532925
            if self.game.players[self.index-1].hit_side and not self.game.players[self.index-1].hit_top and self.game.players[self.index-1].counter == 3:
                print("side")
                self.game.first_hit = False
                self.game.players[self.index-1].angle = -(self.game.players[self.index-1].angle + 180 * 0.0174532925)
            if not self.game.players[self.index-1].hit_side and self.game.players[self.index-1].hit_top and self.counter == 3:
                print("top")
                self.game.first_hit = False
                self.game.players[self.index-1].angle = -(self.game.players[self.index-1].angle + 360 * 0.0174532925)
            
    def checkMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.pressed = pygame.mouse.get_pressed()

        if not self.pressed[0]:
            if not self.first_time:
                self.speed = math.sqrt(self.pos_end[0] ** 2 + self.pos_end[1] ** 2) / 15
                pygame.draw.circle(self.game.players[self.index].image, RED, (self.radius, self.radius), self.radius)
                self.index += 1
                if self.index > len(self.game.players) - 1:
                    self.index = 0
            
            self.first_time = True

        if self.pressed[0] and self.game.players[self.index].rect.collidepoint(self.mouse_pos) and self.speed <= 0.1:
            if self.first_time:
                self.pos_start = (self.mouse_pos[0], self.mouse_pos[1])
                self.first_time = False
        if self.pressed[0] and not self.first_time and self.speed <= 0.1:
            self.pos_end = ((self.mouse_pos[0] - self.pos_start[0]), (self.mouse_pos[1] - self.pos_start[1]))
            self.angle = math.atan2(self.pos_end[1], self.pos_end[0])
            self.hit = False

    def movement(self):
        pygame.draw.circle(self.game.players[self.index].image, BLUE, (self.radius, self.radius), self.radius)
        self.checkMouse()
        if self.game.players[self.index-1].speed > 0.1 and not self.game.first_hit: 
                self.copy = self.game.players[self.index-1].rect.copy()
                self.collide()
                self.game.players[self.index-1].rect.x -= self.speed * math.cos(self.game.players[self.index-1].angle)
                self.game.players[self.index-1].rect.y -= self.speed * math.sin(self.game.players[self.index-1].angle)
        elif self.game.players[self.index-1].speed > 0.1 and self.game.first_hit:
            self.collide()
        self.speed = self.speed * 0.95

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.surface.Surface([self.width, self.height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.game.block_list.append(self.rect)





            
            
