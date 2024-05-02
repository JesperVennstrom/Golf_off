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

    def new(self):
        self.playing = True

        self.all_sprites   = pygame.sprite.LayeredUpdates()
        self.blocks        = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.goal          = pygame.sprite.LayeredUpdates()
        self.hill          = pygame.sprite.LayeredUpdates()
        self.pit           = pygame.sprite.LayeredUpdates()
        map = Image.open('img/frame-1-_1_.ppm')
        print(map)

        self.block_list = []
        self.players = []
        self.first_hit = False
        self.players.append(Player(self, 10, 10))
        self.generateTilemap()

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
                if column == 2:
                    GroundCorner(self, j, i, 4)
                if column == 3:
                    Goal(self, j, i)
                    Ground(self, j, i)
                if column == 4:
                    Hill(self, j, i, 4, 0.1)

    def draw(self):
        self.screen.fill(BROWN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        if not self.first_hit:
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