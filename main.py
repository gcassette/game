import pygame

# Define our square object and call super to
# give it all the properties and methods of pygame.sprite.Sprite
# Define the class for our square objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed_x = 0
        self.speed_y = 0
    def update(self):
        keys = pygame.key.get_pressed()
        
        self.speed_x = 0
        self.speed_y = 0
        
        if keys[pygame.K_LEFT]:
            self.speed_x = -1
        if keys[pygame.K_RIGHT]:
            self.speed_x = 1
        if keys[pygame.K_UP]:
            self.speed_y = -1
        if keys[pygame.K_DOWN]:
            self.speed_y = 1
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello Pygame")

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    # Update the display using flip
    pygame.display.flip()

# Quit Pygame
pygame.quit()