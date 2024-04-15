import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.player_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = PLAYER_LAYER
        self.radius = TILESIZE // 2
        
        self.index = 0

        self.hit = False

        self.first_time = True
        self.speed = 0
        self.pos_start = (0, 0)
        self.pos_end = (0, 0)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.angle = 0

        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)

    def update(self):
        self.rect = self.image.get_rect(center=(self.x + self.radius, self.y + self.radius))
        self.prev_x = self.x
        self.prev_y = self.y
        self.movement()

        # In your main game loop or collision detection logic:
        for block in self.game.blocks:
            if pygame.sprite.collide_rect(self.game.players[self.index], block):
                self.kill()
                collision_side = self.game.players[self.index].collision_side(block)
                if collision_side:
                    print("Collision from:", collision_side)

    def collision_side(self, block):
        # Compare positions to determine collision side
        if self.prev_x < block.rect.left:  # Collision from left
            return "left"
        elif self.prev_x > block.rect.right:  # Collision from right
            return "right"
        elif self.prev_y < block.rect.top:  # Collision from top
            return "top"
        elif self.prev_y > block.rect.bottom:  # Collision from bottom
            return "bottom"
        else:
            return None  # No collision


    def checkMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.pressed = pygame.mouse.get_pressed()

        if not self.pressed[0]:
            if not self.first_time:
                self.speed = math.sqrt(self.pos_end[0] ** 2 + self.pos_end[1] ** 2) / 20
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
        if self.speed > 0.1: 
                self.game.players[self.index-1].x -= self.speed * math.cos(self.angle)
                self.game.players[self.index-1].y -= self.speed * math.sin(self.angle)
        self.speed = self.speed * 0.95

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.surface.Surface([self.width, self.height])
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



            
            
