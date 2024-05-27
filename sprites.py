import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, id, color):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.player_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.radius = TILESIZE // 2
        
        self.id = id


        self.total_x = 0
        self.total_y = 0


        self.hits = False
        self.game.first_hit = False
        self.counter = 1
        self.hit_side = False
        self.hit_top = False

        self.first_time = True
        self.stop = False
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

        self.debuff = 0

        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect.x = self.x
        self.rect.y = self.y

        self.center = pygame.sprite.Sprite()
        pygame.sprite.Sprite.__init__(self.center, self.groups) 
        self.center.image = pygame.Surface((1, 1))
        self.center.rect = pygame.draw.circle(self.center.image, TRANSPARENT, (self.radius, self.radius), 1)
        self.center.rect.x = self.rect.centerx
        self.center.rect.y = self.rect.centery

        self.copy = self.rect.copy()

    def update(self):
        if not self.stop:
            self.movement()
        if self.game.players[self.game.index] == self:
            self.cameraMove()
        self.win()
        self.collideMap()

    def hillPitCollide(self):
        hits_hill = pygame.sprite.spritecollide(self, self.game.hill, False)
        if hits_hill:
            hits_circle = pygame.sprite.collide_circle(self.center, hits_hill[0])
            if hits_circle:
                if abs(hits_hill[0].rect.centerx - self.rect.centerx) > 0.05*hits_hill[0].width or abs(hits_hill[0].rect.centery - self.rect.centery) > 0.05*hits_hill[0].height:
                    hill_angle = math.atan2(hits_hill[0].rect.centery - self.rect.centery, hits_hill[0].rect.centerx - self.rect.centerx)
                    self.speed = math.sqrt((hits_hill[0].speed * math.cos(hill_angle) + self.speed * math.cos(self.angle)) ** 2 + (hits_hill[0].speed * math.sin(hill_angle) + self.speed * math.sin(self.angle)) ** 2)
                    self.angle = math.atan2(hits_hill[0].speed * math.sin(hill_angle) + self.speed * math.sin(self.angle), hits_hill[0].speed * math.cos(hill_angle) + self.speed * math.cos(self.angle))
        return hits_hill
    
    def collidePlayer(self):
        for sprite in self.game.players:
            if sprite != self:
                hits = pygame.sprite.collide_circle(self, sprite)
                if hits and sprite.score != 0 and self.score != 0:
                    speed = 3
                    angle = math.atan2(sprite.rect.centery - self.rect.centery, sprite.rect.centerx - self.rect.centerx)
                    self.speed = math.sqrt((speed * math.cos(angle) + self.speed * math.cos(self.angle)) ** 2 + (speed * math.sin(angle) + self.speed * math.sin(self.angle)) ** 2)
                    self.angle = math.atan2(speed * math.sin(angle) + self.speed * math.sin(self.angle), speed * math.cos(angle) + self.speed * math.cos(self.angle))
                    sprite.speed = self.speed
                    sprite.angle = math.atan2(self.rect.centery - sprite.rect.centery, self.rect.centerx - sprite.rect.centerx)
    def goalCollide(self):
        for sprite in self.game.goal:
            self.goal = sprite
    def win(self):
        hits = False
        self.goalCollide()
        hits = pygame.sprite.collide_circle(self.goal, self.center)
            
        if hits and self.speed < 0.1:
            print("You win!")
            self.game.index += 1
            if self.game.index > len(self.game.players)-1:
                self.game.index = 0
            self.x_offset = self.game.players[self.game.index].rect.centerx - self.game.players[self.game.index-1].rect.centerx
            self.y_offset = self.game.players[self.game.index].rect.centery - self.game.players[self.game.index-1].rect.centery
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.x_offset
                sprite.rect.y -= self.y_offset
            for sprite in self.game.players:
                sprite.copy.x -= self.x_offset
                sprite.copy.y -= self.y_offset
            self.kill()
            self.game.players.remove(self)
            if self.game.index != 0:
                self.game.index -= 1
            self.game.recent_score[self.id] = self.score
            self.game.scores[self.id] += self.score

    def moveX(self):
        self.rect.x -= self.speed * math.cos(self.angle)
        self.total_x -= self.speed * math.cos(self.angle)
        self.center.rect.x = self.rect.centerx
        if self.game.players[self.game.index] == self:
            for sprite in self.game.all_sprites:
                sprite.rect.x += self.speed * math.cos(self.angle)

            for sprite in self.game.players:
                sprite.copy.x += self.speed * math.cos(self.angle)

        

    def moveY(self):
        self.rect.y -= self.speed * math.sin(self.angle)
        self.total_y -= self.speed * math.sin(self.angle)
        self.center.rect.y = self.rect.centery
        if self.game.players[self.game.index] == self:
            for sprite in self.game.all_sprites:
                sprite.rect.y += self.speed * math.sin(self.angle)
            for sprite in self.game.players:
                sprite.copy.y += self.speed * math.sin(self.angle)

        



    def movement(self):
        if self.game.players[self.game.index] == self:
            self.checkMouse()
            self.collidePlayer()
            self.copy = self.rect.copy()
        
        if self.speed > 0.1:
            self.moveX()
            self.collideX()
            self.moveY()
            self.collideY()
        self.speed = self.speed * 0.97
            
    def collideX(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            for sprite in self.game.all_sprites:
                if sprite != self:
                    sprite.rect.x -= self.speed * math.cos(self.angle)
            for sprite in self.game.players:
                    sprite.copy.x -= self.speed * math.cos(self.angle)
            self.angle = -(self.angle + 180 * 0.0174532925)

    def collideY(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits: 
            for sprite in self.game.all_sprites:
                if sprite != self:
                    sprite.rect.y -= self.speed * math.sin(self.angle)
            for sprite in self.game.players:
                sprite.copy.y -= self.speed * math.sin(self.angle)
            self.angle = -(self.angle + 360 * 0.0174532925)

    def collideMap(self):
        self.hillPitCollide()
        self.waterCollide(False)

    def waterCollide(self, called_by_wall):

        hits = pygame.sprite.spritecollide(self, self.game.water, False)
        if hits:
            if self.speed < 4:
                self.speed = 0
                if self.game.players[self.game.index] == self and not called_by_wall:
                    for sprite in self.game.all_sprites:
                        if sprite != self:
                            sprite.rect.x += self.total_x
                            sprite.rect.y += self.total_y
                    for sprite in self.game.players:
                        sprite.copy.x += self.total_x
                        sprite.copy.y += self.total_y
                else:
                    self.rect = self.copy
                    self.debuff = random.randint(-60, 60)
                    self.speed = 0
                    print(self.speed)
                    self.copy = self.rect.copy()
            else:
                self.speed = self.speed * 0.90



            
    def checkMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.pressed = pygame.mouse.get_pressed()

        if not self.pressed[0]:
            if not self.first_time:
                self.speed = math.sqrt(self.pos_end[0] ** 2 + self.pos_end[1] ** 2) / 10
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
                for sprite in self.game.players:
                    sprite.copy.x -= self.x_offset
                    sprite.copy.y -= self.y_offset
                self.switch = False
                self.copy = self.rect.copy()
                self.debuff = 0

        if self.pressed[0] and self.rect.collidepoint(self.mouse_pos) and self.speed <= 0.1:
            if self.first_time:
                self.pos_start = (self.mouse_pos[0], self.mouse_pos[1])
                self.first_time = False
                self.total_x = 0
                self.total_y = 0
        if self.pressed[0] and not self.first_time and self.speed <= 0.1:
            self.pos_end = ((self.mouse_pos[0] - self.pos_start[0]), (self.mouse_pos[1] - self.pos_start[1]))
            self.angle = math.atan2(self.pos_end[1], self.pos_end[0]) + self.debuff * 0.0174532925
            self.hit = False
            if self.debuff == 0:
                color = WHITE
            else:
                color = RED
            self.game.drawDirection(self.pos_end, color)

    def cameraMove(self):
        if self.speed < 0.1:
            keys = pygame.key.get_pressed()
            speed_multiplier = 1
            if keys[pygame.K_LSHIFT]:
                speed_multiplier = 3
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                self.stop = True
            if keys[pygame.K_w]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += 5 * speed_multiplier
            if keys[pygame.K_s]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= 5 * speed_multiplier
            if keys[pygame.K_a]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += 5 * speed_multiplier
            if keys[pygame.K_d]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 5 * speed_multiplier
            if keys[pygame.K_SPACE]:
                self.stop = False
                y_offset = self.rect.centery - WIN_HEIGHT/2
                x_offset = self.rect.centerx - WIN_WIDTH/2
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= x_offset
                    sprite.rect.y -= y_offset
                for sprite in self.game.players:
                    sprite.copy.x -= x_offset
                    sprite.copy.y -= y_offset


class Wall(pygame.sprite.Sprite):
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
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = CIRCLE_LAYER
        self.groups = self.game.all_sprites, self.game.water
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.surface.Surface([self.width, self.height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



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

class WallOfDestruction(pygame.sprite.Sprite):
    def __init__(self, game, x, y, move_x, move_y, speed):
        self.groups = game.all_sprites, game.blocks
        self.game = game
        self._layer = MOVING_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.facing_x = "right"
        self.facing_y = "up"
        self.movement_loop_x = 0
        self.movement_loop_y = 0

        self.max_x = move_x * TILESIZE
        self.max_y = move_y * TILESIZE

        self.speed = speed

        self.image = pygame.surface.Surface([self.width, self.height])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        self.moveX()
        self.moveY()
        self.collide()

    def moveX(self):
        if self.max_x != 0:
            if self.facing_x == 'left':
                self.rect.x -= self.speed
                self.movement_loop_x -= self.speed
                if self.movement_loop_x <= 0:
                    self.facing_x = 'right'
            if self.facing_x == 'right':
                self.rect.x += self.speed
                self.movement_loop_x += self.speed
                if self.movement_loop_x >= self.max_x:
                    self.facing_x = 'left'
    def moveY(self):
        if self.max_y:
            if self.facing_y == 'up':
                self.rect.y -= self.speed
                self.movement_loop_y -= self.speed
                if self.movement_loop_y <= 0:
                    self.facing_y = 'down'
            if self.facing_y == 'down':
                self.rect.y += self.speed
                self.movement_loop_y += self.speed
                if self.movement_loop_y >= self.max_y:
                    self.facing_y = 'up'
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            if self.max_x != 0:    
                if self.facing_x == 'left':
                    hits[0].rect.x -= self.speed+1
                    if self.game.players[self.game.index] == hits[0]:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x += self.speed+1
                if self.facing_x == 'right':
                    hits[0].rect.x += self.speed+1
                    if self.game.players[self.game.index] == hits[0]:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= self.speed+1
            if self.max_y != 0:
                if self.facing_y == 'up':
                    hits[0].rect.y -= self.speed +1
                    if self.game.players[self.game.index] == hits[0]:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += self.speed+1
                if self.facing_y == 'down':
                    hits[0].rect.y += self.speed+1
                    if self.game.players[self.game.index] == hits[0]:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= self.speed+1
            hits[0].waterCollide(True)



class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("comici.ttf", fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center =(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
    def isPressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    

            
            
