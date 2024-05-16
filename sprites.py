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
        
        self.hits = False
        self.game.first_hit = False
        self.counter = 1
        self.hit_side = False
        self.hit_top = False

        self.first_time = True
        
        self.score = 0
        self.x_offset = 0
        self.y_offset = 0

        self.speed = 0
        self.pos_start = (0, 0)
        self.pos_end = (0, 0)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.switch = False

        self.angle = 0

        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect.x = self.x
        self.rect.y = self.y

        self.center = pygame.sprite.Sprite()
        pygame.sprite.Sprite.__init__(self.center, self.groups) 
        self.center.image = pygame.Surface((1, 1))
        self.center.rect = pygame.draw.circle(self.center.image, TRANSPARENT, (self.radius, self.radius), 1)
        self.center.rect.x = self.rect.centerx
        self.center.rect.y = self.rect.centery


    def update(self):
        self.movement()
        self.win()
        self.hillPitCollide()

    def hillPitCollide(self):
        hits_hill = pygame.sprite.spritecollide(self, self.game.hill, False)
        if hits_hill:
            hits_circle = pygame.sprite.collide_circle(self.center, hits_hill[0])
            if hits_circle:
                if abs(hits_hill[0].rect.centerx - self.rect.centerx) > 2 or abs(hits_hill[0].rect.centery - self.rect.centery) > 2:
                    hill_angle = math.atan2(hits_hill[0].rect.centery - self.rect.centery, hits_hill[0].rect.centerx - self.rect.centerx)
                    self.speed = math.sqrt((hits_hill[0].speed * math.cos(hill_angle) + self.speed * math.cos(self.angle)) ** 2 + (hits_hill[0].speed * math.sin(hill_angle) + self.speed * math.sin(self.angle)) ** 2)
                    self.angle = math.atan2(hits_hill[0].speed * math.sin(hill_angle) + self.speed * math.sin(self.angle), hits_hill[0].speed * math.cos(hill_angle) + self.speed * math.cos(self.angle))



    def goalCollide(self):
        for sprite in self.game.goal:
            self.goal = sprite
    def win(self):
        hits = False
        self.goalCollide()
        hits = pygame.sprite.collide_circle(self.goal, self.center)
            
        if hits and self.speed < 0.1:
            print("You win!")
            self.kill()
            self.game.index+=1
            if self.game.index > len(self.game.players)-1:
                self.game.index = 0
            self.x_offset = self.game.players[self.game.index].rect.centerx - self.game.players[self.game.index-1].rect.centerx
            self.y_offset = self.game.players[self.game.index].rect.centery - self.game.players[self.game.index-1].rect.centery
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.x_offset
                sprite.rect.y -= self.y_offset
            self.game.players.remove(self)
            if self.game.index > len(self.game.players)-1:
                self.game.index = 0

    def moveX(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.center.rect.x = self.rect.centerx
        for sprite in self.game.all_sprites:
            sprite.rect.x += self.speed * math.cos(self.angle)

    def moveY(self):
        self.rect.y -= self.speed * math.sin(self.angle)
        self.center.rect.y = self.rect.centery
        for sprite in self.game.all_sprites:
            sprite.rect.y += self.speed * math.sin(self.angle)

        



    def movement(self):
        if self.game.players[self.game.index] == self:
            pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
            self.checkMouse()
        else:
            pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        if self.speed > 0.1:
            self.moveX()
            self.collideX()
            self.moveY()
            self.collideY()
        self.speed = self.speed * 0.97
            
    def collideX(self):
        block_rect = self.game.block_list[0].unionall(self.game.block_list)
        self.hits = block_rect.contains((self.rect))
        if not self.hits:
            for sprite in self.game.all_sprites:
                if sprite != self:
                    sprite.rect.x -= self.speed * math.cos(self.angle)
            self.angle = -(self.angle + 180 * 0.0174532925)
            print("hitx")

    def collideY(self):
        block_rect = self.game.block_list[0].unionall(self.game.block_list)
        self.hits = block_rect.contains((self.rect))
        if not self.hits: 
            for sprite in self.game.all_sprites:
                if sprite != self:
                    sprite.rect.y -= self.speed * math.sin(self.angle)
            self.angle = -(self.angle + 360 * 0.0174532925)
            print("hitY")


            
    def checkMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.pressed = pygame.mouse.get_pressed()

        if not self.pressed[0]:
            if not self.first_time:
                self.speed = math.sqrt(self.pos_end[0] ** 2 + self.pos_end[1] ** 2) / 20
                self = self
                self.score += 1
                self.switch = True
            self.first_time = True
            if self.switch and self.speed < 0.1:
                self.game.index += 1
                if self.game.index > len(self.game.players)-1:
                    self.game.index = 0
                self.x_offset = self.game.players[self.game.index].rect.centerx - self.game.players[self.game.index-1].rect.centerx
                self.y_offset = self.game.players[self.game.index].rect.centery - self.game.players[self.game.index-1].rect.centery
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= self.x_offset
                    sprite.rect.y -= self.y_offset
                self.switch = False

        if self.pressed[0] and self.rect.collidepoint(self.mouse_pos) and self.speed <= 0.1:
            if self.first_time:
                self.pos_start = (self.mouse_pos[0], self.mouse_pos[1])
                self.first_time = False
        if self.pressed[0] and not self.first_time and self.speed <= 0.1:
            self.pos_end = ((self.mouse_pos[0] - self.pos_start[0]), (self.mouse_pos[1] - self.pos_start[1]))
            self.angle = math.atan2(self.pos_end[1], self.pos_end[0])
            self.hit = False


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

class GroundCorner(pygame.sprite.Sprite):
    def __init__(self, game, x, y, radius):
        self.game = game
        self._layer = CIRCLE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * radius
        self.height = TILESIZE * radius
        
        self.radius = (radius * TILESIZE) / 2
        self.image = pygame.surface.Surface ((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.image, GREEN, pygame.Rect(0,0,self.width,self.height), border_radius=self.width)
        self.rect.x = self.x - self.radius / 2
        self.rect.y = self.y - self.radius / 2

        self.game.block_list.append(self.rect)


class Goal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GOAL_LAYER
        self.groups = self.game.all_sprites, self.game.goal
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        self.radius = TILESIZE // 2
        self.image = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, BLACK, (self.radius, self.radius), self.radius)
        self.rect.x = self.x
        self.rect.y = self.y

class Hill(pygame.sprite.Sprite):
    def __init__(self, game, x, y, radius, speed):
        self.game = game
        self._layer = CIRCLE_LAYER
        self.groups = self.game.all_sprites, self.game.hill
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * radius
        self.height = TILESIZE * radius
        self.color = LIGHT_GREEN
        
        self.speed = speed

        self.radius = (radius * TILESIZE) / 2
        self.image = pygame.surface.Surface ((self.width, self.height), pygame.SRCALPHA)
       # Define colors for gradient
        start_color = (0, 200, 0)
        mid_color = (144, 235, 144)

        color_steps = []
        for i in range(3):
            color_steps.append([(mid_color[i] - start_color[i]) / (self.radius / 5) * (1 - math.cos((math.pi / 2) * (j / 2 / 5))) for j in range(int(self.radius / 5) * 5)])

        # Draw concentric circles with gradient
        current_color = start_color
        for step in range(int(self.radius), 0, -5):
            color = tuple(int(max(min(current_color[j] + color_steps[j][min(step // 5, len(color_steps[j]) - 1)], mid_color[j]), start_color[j])) for j in range(3))
            pygame.draw.circle(self.image, color, (int(self.radius), int(self.radius)), step)
            current_color = color

        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.radius / 2
        self.rect.y = self.y - self.radius / 2

        self.game.block_list.append(self.rect)
class Pit(pygame.sprite.Sprite):
    def __init__(self, game, x, y, radius, speed):
        self.game = game
        self._layer = CIRCLE_LAYER
        self.groups = self.game.all_sprites, self.game.hill
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * radius
        self.height = TILESIZE * radius
        self.color = GREEN
        
        self.speed = -speed

        self.radius = (radius * TILESIZE) / 2
        self.image = pygame.surface.Surface ((self.width, self.height), pygame.SRCALPHA)

        i = self.width
        segment_width = 5  # Desired width of each segment
        while i > 0:
            step = max(segment_width, int(i / 20))  # Adjust step size
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), int(i/2), segment_width)
            i -= step
            self.color = (self.color[0], max(self.color[1] - step, 100), self.color[2])

        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.radius / 2
        self.rect.y = self.y - self.radius / 2

        self.game.block_list.append(self.rect)

            
            
