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

        self.center = pygame.sprite.Sprite()
        pygame.sprite.Sprite.__init__(self.center, self.groups) 
        self.center.image = pygame.Surface((1, 1))
        self.center.rect = pygame.draw.circle(self.center.image, BLACK, (self.radius, self.radius), 1)
        self.center.rect.x = self.rect.centerx
        self.center.rect.y = self.rect.centery


    def update(self):
        self.collide()
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
            
    def collide(self):
        block_rect = self.game.block_list[0].unionall(self.game.block_list)
        self.game.players[self.index-1].hits = block_rect.contains((self.game.players[self.index-1].rect))

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
                self.game.players[self.index-1].angle = -(self.game.players[self.index-1].angle + 180 * 0.0174532925 + 360 * 0.0174532925)

            if not self.game.players[self.index-1].hit_side and not self.game.players[self.index-1].hit_top and self.game.players[self.index-1].counter == 3:
                print("nothing")
                self.game.first_hit = False
                self.game.players[self.index-1].angle = -(self.game.players[self.index-1].angle + 180 * 0.0174532925 + 360 * 0.0174532925)
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
                self.game.players[self.index].speed = math.sqrt(self.game.players[self.index].pos_end[0] ** 2 + self.game.players[self.index].pos_end[1] ** 2) / 20
                pygame.draw.circle(self.game.players[self.index].image, RED, (self.radius, self.radius), self.radius)
                self.index += 1
                if self.index > len(self.game.players) - 1:
                    self.index = 0
            
            self.game.players[self.index].first_time = True

        if self.game.players[self.index].pressed[0] and self.game.players[self.index].rect.collidepoint(self.mouse_pos) and self.game.players[self.index].speed <= 0.1:
            if self.game.players[self.index].first_time:
                self.game.players[self.index].pos_start = (self.mouse_pos[0], self.mouse_pos[1])
                self.game.players[self.index].first_time = False
        if self.pressed[0] and not self.first_time and self.speed <= 0.1:
            self.game.players[self.index].pos_end = ((self.mouse_pos[0] - self.pos_start[0]), (self.mouse_pos[1] - self.pos_start[1]))
            self.angle = math.atan2(self.pos_end[1], self.pos_end[0])
            self.game.players[self.index].hit = False

    def movement(self):
        pygame.draw.circle(self.game.players[self.index].image, BLUE, (self.radius, self.radius), self.radius)
        self.checkMouse()
        if self.game.players[self.index-1].speed > 0.1 and not self.game.first_hit: 
                self.copy = self.game.players[self.index-1].rect.copy()
                self.collide()
                self.game.players[self.index-1].rect.x -= self.game.players[self.index-1].speed * math.cos(self.game.players[self.index-1].angle)
                self.game.players[self.index-1].rect.y -= self.game.players[self.index-1].speed * math.sin(self.game.players[self.index-1].angle)
                self.center.rect.x = self.game.players[self.index-1].rect.centerx
                self.center.rect.y = self.game.players[self.index-1].rect.centery
        elif self.game.players[self.index-1].speed > 0.1 and self.game.first_hit:
            self.collide()
        self.speed = self.speed * 0.97

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

            
            
