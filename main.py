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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.running = True

        self.index = 0

    def new(self):
        self.playing = True

        self.all_sprites   = pygame.sprite.LayeredUpdates()
        self.blocks        = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.goal          = pygame.sprite.LayeredUpdates()
        self.hill          = pygame.sprite.LayeredUpdates()
        self.pit           = pygame.sprite.LayeredUpdates()
        map = Image.open('img/frame-1-_1_.ppm')

        self.block_list = []
        self.players = []
        self.first_hit = False
        self.players.append(Player(self, 10, 12))
        self.players.append(Player(self, 10, 12))
        self.players.append(Player(self, 10, 12))
        self.players.append(Player(self, 10, 12))
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
        self.running = False

#    def create_tilemap(self):
#        # Open the image
#        img = Image.open("img/frame-2-_1_.ppm")
#        
#        # Convert the image to grayscale
#        img = img.convert('L') # 'L' mode means grayscale
#        
#        # Get image dimensions
#        width, height = img.size
#        
#        # Create an empty list to store the tilemap
#        self.map = []
#        
#        # Iterate through the image and extract tiles
#        for y in range(width):
#            row = []
#            for x in range(height):
#                # Crop the tile from the image
#                tile = img.crop((x, y, (x + 1), (y + 1)))
#                # Convert the tile to a list of RGB values
#                tile_colors = list(tile.getdata())
#                # Append the tile colors to the row
#                row.append(tile_colors)
#            # Append the row to the tilemap
#            self.map.append(row)
#    
    def generateTilemap(self):
#        self.create_tilemap()
#        print(self.map)
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                if column == 1:
                    Ground(self, j, i)
                elif column == 2:
                    GroundCorner(self, j, i, 4)
                elif column == 3:
                    Goal(self, j, i)
                    Ground(self, j, i)
                    Pit(self, j, i, 2, 0.1)
                elif column == 4:
                    Hill(self, j, i, 4, 0.1)
                elif column == 5:
                    Pit(self, j, i, 6, 0.2  )

    def draw(self):
        self.screen.fill(BROWN)
        self.all_sprites.draw(self.screen)
        if self.players:
            self.screen.blit(pygame.font.Font.render(self.font, str(self.players[self.index].score), True, BLACK), (WIN_WIDTH/2, 10))
        self.clock.tick(FPS)
        pygame.display.update()

    def update(self):
        self.all_sprites.update()

    def endScreen(self):
        pass

    def introScreen(self):
        pass

g = Game()
g.introScreen()
g.new()
while g.running:
    g.main()
    g.endScreen()

pygame.quit()
sys.exit()