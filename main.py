import pygame
from config import *
from sprites import *
from PIL import Image
import sys

class Game: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GOLF OFF")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.minimap = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("comici.ttf", 32)
        self.running = True

        self.index = 0
        self.directionImage = None

        self.colors = [BLUE, RED, PURPLE, WHITE]

    def new(self):
        self.playing = True

        self.all_sprites   = pygame.sprite.LayeredUpdates()
        self.blocks        = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.goal          = pygame.sprite.LayeredUpdates()
        self.hill          = pygame.sprite.LayeredUpdates()
        self.pit           = pygame.sprite.LayeredUpdates()
        self.water         = pygame.sprite.LayeredUpdates()
        map = Image.open('img/frame-1-_1_.ppm')

        self.players = []
        self.first_hit = False
        self.generateTilemap()
        self.y_offset = self.players[0].rect.centery - WIN_HEIGHT/2
        self.x_offset = self.players[0].rect.centerx - WIN_WIDTH/2
        for sprite in self.all_sprites:
            sprite.rect.x -= self.x_offset
            sprite.rect.y -= self.y_offset
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if not self.players:
                self.playing = False
                for sprite in self.all_sprites:
                    sprite.kill()
        self.callScoreboard()
        self.running = False

    def create_tilemap(self):
        # Open the image
        img = Image.open("img/golf_map2.png")
        
        # Convert the image to grayscale
        img = img.convert('RGB')
        
        # Get image dimensions
        height, width = img.size
        
        # Create an empty list to store the tilemap
        self.map = []
        
        # Iterate through the image and extract tiles
        for y in range(width):
            row = []
            for x in range(height):
                # Crop the tile from the image
                tile = img.crop((x, y, (x + 1), (y + 1)))
                # Convert the tile to a list of RGB values
                tile_colors = list(tile.getdata())
                # Append the tile colors to the row
                row.append(tile_colors)
            # Append the row to the tilemap
            self.map.append(row)
    
    def generateTilemap(self):
        self.create_tilemap()
        for i, row in enumerate(self.map):
            for j, column in enumerate(row):
                if column == [(0,0,0)]:
                    Wall(self, j, i)
                elif column == [(134,134,134)]:
                    Goal(self, j, i)
                    Pit(self, j, i, 2, 0.1)
                elif column[0][0] == 50:
                    radius = column[0][1]
                    steepness = column[0][2] / 10
                    Hill(self, j, i, radius, steepness)
                elif column[0][0] == 100:
                    radius = column[0][1]
                    steepness = column[0][2] / 10
                    Pit(self, j, i, radius, steepness)
                elif column == [(0,0,255)]:
                    Water(self, j, i)
                elif column ==[(211, 211, 211)]:
                    for u in range(self.count):
                        print("Player", i, j)
                        color_index = random.randint(0, len(self.colors) - 1)
                        self.players.append(Player(self, j, i, u, self.colors[color_index]))
                        self.colors.pop(color_index)
                    self.scores = [0 for u in range(self.count)]
                    self.recent_score = [0 for u in range(self.count)]

        self.minimap.fill(GREEN)
        for sprite in self.all_sprites:
                minisprite = pygame.transform.scale(sprite.image, (1, 1))
                self.minimap.blit(minisprite, (sprite.rect.x/30, sprite.rect.y/30))

        self.minimap_border = pygame.surface.Surface((110, 110), pygame.SRCALPHA)
        pygame.draw.rect(self.minimap_border, BLACK, (0, 0, 110, 110), 5)


                    

    def draw(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        if self.directionImage:
            self.screen.blit(self.directionImage, (0, 0))
            self.directionImage = None
        if self.players:
            self.screen.blit(pygame.font.Font.render(self.font, str(self.players[self.index].score), True, BLACK), (WIN_WIDTH/2, 10))
        self.screen.blit(self.minimap_border, (0, 0))
        self.screen.blit(self.minimap, (5, 5))
        self.clock.tick(FPS)
        pygame.display.update()

    def drawDirection(self, pos):
        self.directionImage = pygame.surface.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(self.directionImage, WHITE, (WIN_WIDTH/2 - pos[0], WIN_HEIGHT/2 - pos[1]), 5)



    def update(self):
        self.all_sprites.update()

    def endScreen(self):
        pass

    def introScreen(self):
        intro = True
        text = self.font.render("Golf Off", True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        start_text = self.font.render("Select Player Amount", True, BLACK)
        start_rect = start_text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        start_button = Button(WIN_WIDTH/2 - 50, 350, 100, 50, BLACK, WHITE, "Start", 32)
        option_1 = Button(WIN_WIDTH/2 - 220, 350, 100, 50, BLACK, WHITE, "1", 32)
        option_2 = Button(WIN_WIDTH/2 - 110, 350, 100, 50, BLACK, WHITE, "2", 32)
        option_3 = Button(WIN_WIDTH/2 + 10, 350, 100, 50, BLACK, WHITE, "3", 32)
        option_4 = Button(WIN_WIDTH/2 + 120, 350, 100, 50, BLACK, WHITE, "4", 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                intro = False
            self.clock.tick(FPS)
            self.screen.fill(PURPLE)
            self.screen.blit(text, text_rect)
            self.screen.blit(start_button.image, start_button.rect)
            pygame.display.update()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if start_button.isPressed(mouse_pos, mouse_pressed):
                intro = False
                start = True
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    self.running = False
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if option_1.isPressed(mouse_pos, mouse_pressed):
                    self.count = 1
                    start = False
                elif option_2.isPressed(mouse_pos, mouse_pressed):
                    self.count = 2
                    start = False
                elif option_3.isPressed(mouse_pos, mouse_pressed):
                    self.count = 3
                    start = False
                elif option_4.isPressed(mouse_pos, mouse_pressed):
                    self.count = 4
                    start = False
            self.screen.fill(PURPLE)
            self.screen.blit(option_1.image, option_1.rect)
            self.screen.blit(option_2.image, option_2.rect)
            self.screen.blit(option_3.image, option_3.rect)
            self.screen.blit(option_4.image, option_4.rect)
            self.screen.blit(start_text, start_rect)

            pygame.display.update()
    def defineScoreboard(self):
        pressed = False
        self.scoreboard = pygame.surface.Surface((500, 500), pygame.SRCALPHA)
        self.scoreboard.fill(TRANSPARENT)
        pygame.draw.rect(self.scoreboard, MAROON, (0, 0, 500, 100))
        for i in range(self.count):
            pygame.draw.rect(self.scoreboard, BEIGE, (0, 100 * (i+1), 500, 100))
            pygame.draw.rect(self.scoreboard, MAROON, (0, 100 * (i+1), 500, 100), 5)
            self.scoreboard.blit(pygame.font.Font.render(self.font, "Player " + str(i+1), True, BLACK), (10, 100 * (i+1) + 20))
            self.scoreboard.blit(pygame.font.Font.render(self.font, "Score: " + str(self.recent_score[i]), True, BLACK), (175, 100 * (i+1) + 20))
            self.scoreboard.blit(pygame.font.Font.render(self.font, "Total: " + str(self.scores[i]), True, BLACK), (350, 100 * (i+1) + 20))
    def callScoreboard(self):
        self.defineScoreboard()
        while not pressed:
            self.screen.fill(PURPLE)
            self.screen.blit(self.scoreboard, (50, 50))
            pygame.display.update()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                pressed = True

g = Game()
g.introScreen()
g.new()
while g.running:
    g.main()
    g.endScreen()

pygame.quit()
sys.exit()